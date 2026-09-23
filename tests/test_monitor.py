import socket
import time

from infra_watch.monitor import Metric, Snapshot, collect_memory, take_snapshot


def test_metric_thresholds():
    assert Metric("x", 50, "%", threshold_warning=75, threshold_critical=90).evaluate().status == "ok"
    assert Metric("x", 80, "%", threshold_warning=75, threshold_critical=90).evaluate().status == "warning"
    assert Metric("x", 95, "%", threshold_warning=75, threshold_critical=90).evaluate().status == "critical"


def test_snapshot_structure():
    snap = take_snapshot()
    assert snap.hostname == socket.gethostname()
    names = {m.name for m in snap.metrics}
    assert "cpu_usage" in names
    assert "memory_usage" in names
    assert any(n.startswith("disk_usage") for n in names)


def test_worst_status():
    snap = Snapshot(hostname="h", timestamp=time.time())
    assert snap.worst_status == "ok"
    snap.metrics.append(Metric("a", 10, "%", status="critical"))
    snap.metrics.append(Metric("b", 20, "%", status="warning"))
    assert snap.worst_status == "critical"


def test_memory_value_sane():
    m = collect_memory()
    assert 0 <= m.value <= 100
