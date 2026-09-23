from infra_watch.monitor import Metric, Snapshot
from infra_watch.report import render_html
import time


def test_render_html_contains_metrics():
    snap = Snapshot(hostname="test-host", timestamp=time.time())
    snap.metrics.append(Metric("cpu_usage", 42.0, "%", status="ok"))
    snap.metrics.append(Metric("memory_usage", 91.0, "%", status="critical"))
    html = render_html(snap)
    assert "cpu_usage" in html
    assert "CRITIQUE" in html
    assert "test-host" in html
