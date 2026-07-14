from __future__ import annotations

from pathlib import Path

from scripts.repository_audit import audit
from scripts.security_scan import scan

ROOT = Path(__file__).resolve().parents[1]


def test_repository_alignment_audit_has_no_blocking_findings() -> None:
    result = audit(ROOT)
    assert result["status"] == "pass", result["findings"]


def test_security_scan_has_no_blocking_findings() -> None:
    result = scan(ROOT)
    assert result["status"] == "pass", result["findings"]


def test_core_markdown_links_resolve() -> None:
    result = audit(ROOT)
    broken = [
        item for item in result["findings"]
        if item["severity"] == "high" and "Broken local link" in item["message"]
    ]
    assert broken == []


def test_dashboard_has_all_submission_tabs() -> None:
    html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
    for tab_id in (
        "overview",
        "operations",
        "edge",
        "live",
        "cost",
        "evidence",
        "ai",
        "architecture",
    ):
        assert f'id="{tab_id}"' in html


def test_transient_directories_are_not_packaged() -> None:
    forbidden_names = {".venv", "venv", "runtime", "logs"}
    present = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_dir() and path.name.lower() in forbidden_names
    ]
    assert present == []
