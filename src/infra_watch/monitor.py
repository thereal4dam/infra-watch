"""Collecte des métriques système : CPU, mémoire, disque, réseau et services.

Conçu pour être léger, sans démon : chaque appel fait un snapshot
de l'état de la machine et retourne un dictionnaire structuré.
"""
from __future__ import annotations

import shutil
import socket
import subprocess
import time
from dataclasses import dataclass, field, asdict
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None


@dataclass
class Metric:
    name: str
    value: float
    unit: str
    status: str = "ok"  # ok | warning | critical
    threshold_warning: float | None = None
    threshold_critical: float | None = None

    def evaluate(self) -> "Metric":
        """Positionne le statut selon les seuils configurés."""
        if self.threshold_critical is not None and self.value >= self.threshold_critical:
            self.status = "critical"
        elif self.threshold_warning is not None and self.value >= self.threshold_warning:
            self.status = "warning"
        return self


@dataclass
class Snapshot:
    hostname: str
    timestamp: float
    metrics: list[Metric] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hostname": self.hostname,
            "timestamp": self.timestamp,
            "metrics": [asdict(m) for m in self.metrics],
        }

    @property
    def worst_status(self) -> str:
        order = {"ok": 0, "warning": 1, "critical": 2}
        if not self.metrics:
            return "ok"
        return max((m.status for m in self.metrics), key=lambda s: order[s])


def collect_cpu(interval: float = 0.5) -> Metric:
    """Taux d'utilisation CPU en pourcentage (moyenne sur tous les cœurs)."""
    if psutil is None:
        raise RuntimeError("psutil est requis : pip install psutil")
    return Metric("cpu_usage", psutil.cpu_percent(interval=interval), "%",
                  threshold_warning=75.0, threshold_critical=90.0).evaluate()


def collect_memory() -> Metric:
    """Pourcentage de mémoire vive utilisée."""
    mem = psutil.virtual_memory()
    return Metric("memory_usage", mem.percent, "%",
                  threshold_warning=80.0, threshold_critical=95.0).evaluate()


def collect_disk(path: str = "/") -> Metric:
    """Pourcentage d'espace disque occupé sur le point de montage donné."""
    usage = shutil.disk_usage(path)
    percent = round(usage.used / usage.total * 100, 2)
    return Metric(f"disk_usage[{path}]", percent, "%",
                  threshold_warning=85.0, threshold_critical=95.0).evaluate()


def collect_network() -> Metric:
    """Nombre de connexions réseau actives (TCP/UDP établies)."""
    connections = psutil.net_connections(kind="inet")
    active = sum(1 for c in connections if c.status == "ESTABLISHED")
    return Metric("active_connections", float(active), "conn").evaluate()


def check_service(name: str) -> Metric:
    """Vérifie qu'un service systemd est actif (Linux)."""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", name],
            capture_output=True, text=True, timeout=5,
        )
        status = "ok" if result.stdout.strip() == "active" else "critical"
        return Metric(f"service[{name}]", 1.0 if status == "ok" else 0.0, "bool", status)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return Metric(f"service[{name}]", 0.0, "bool", "warning")


def take_snapshot(services: list[str] | None = None,
                  disk_paths: list[str] | None = None) -> Snapshot:
    """Snapshot complet de la machine."""
    snap = Snapshot(hostname=socket.gethostname(), timestamp=time.time())
    snap.metrics.extend([collect_cpu(), collect_memory()])
    for path in (disk_paths or ["/"]):
        snap.metrics.append(collect_disk(path))
    snap.metrics.append(collect_network())
    for svc in (services or []):
        snap.metrics.append(check_service(svc))
    return snap
