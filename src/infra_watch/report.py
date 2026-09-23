"""Génération d'un rapport HTML autonome à partir d'un Snapshot."""
from __future__ import annotations

import datetime
import html

from .monitor import Snapshot

_STATUS_LABEL = {"ok": "OK", "warning": "ATTENTION", "critical": "CRITIQUE"}


def render_html(snapshot: Snapshot) -> str:
    """Retourne un document HTML complet, sans dépendance externe."""
    date = datetime.datetime.fromtimestamp(snapshot.timestamp).strftime("%d/%m/%Y %H:%M:%S")
    rows = []
    for m in snapshot.metrics:
        label = html.escape(_STATUS_LABEL.get(m.status, m.status))
        rows.append(
            f'<tr class="{m.status}"><td>{html.escape(m.name)}</td>'
            f"<td>{m.value:g} {html.escape(m.unit)}</td>"
            f'<td><span class="badge {m.status}">{label}</span></td></tr>'
        )
    worst = snapshot.worst_status
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Rapport InfraWatch - {html.escape(snapshot.hostname)}</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 760px;
         background: #0d1117; color: #e6edf3; }}
  h1 {{ font-size: 1.4rem; }}
  .global {{ padding: .8rem 1rem; border-radius: 8px; font-weight: 600;
             margin-bottom: 1.5rem; }}
  .ok       {{ --c:#3fb950; }} .warning {{ --c:#d29922; }} .critical {{ --c:#f85149; }}
  .global {{ background: color-mix(in srgb, var(--c) 20%, transparent);
            border: 1px solid var(--c); }}
  table {{ width: 100%; border-collapse: collapse; }}
  td, th {{ padding: .6rem .8rem; border-bottom: 1px solid #30363d; text-align: left; }}
  tr {{ border-left: 3px solid var(--c); }}
  .badge {{ color: var(--c); font-weight: 600; }}
  .meta {{ color: #8b949e; font-size: .85rem; margin-bottom: .5rem; }}
</style>
</head>
<body>
  <h1>🖥️ Rapport d'état — {html.escape(snapshot.hostname)}</h1>
  <p class="meta">Généré le {date} par InfraWatch</p>
  <div class="global {worst}">État global : {_STATUS_LABEL[worst]}</div>
  <table>
    <thead><tr><th>Métrique</th><th>Valeur</th><th>Statut</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</body>
</html>"""
