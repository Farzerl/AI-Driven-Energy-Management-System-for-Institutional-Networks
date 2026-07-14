from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cost_dashboard_uses_current_chart_api() -> None:
    javascript = (ROOT / "dashboard" / "static" / "app.js").read_text(
        encoding="utf-8"
    )
    assert 'renderBarChart(\n      "cost-monthly-chart"' in javascript
    assert 'renderBarChart(\n      "cost-scenario-chart"' in javascript


def test_dashboard_asset_has_cache_version() -> None:
    html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
    assert "/static/app.js?v=" in html
