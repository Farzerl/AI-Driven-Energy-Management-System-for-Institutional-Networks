from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_downloaded_repository_contains_submission_runtime_files() -> None:
    required = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "pyproject.toml",
        "src/api/server.py",
        "src/api/evidence_store.py",
        "src/api/cost_store.py",
        "src/api/meter_store.py",
        "src/edge/collector.py",
        "src/edge/buffer.py",
        "src/live/service.py",
        "src/live/model_manager.py",
        "src/costing/model.py",
        "dashboard/index.html",
        "dashboard/static/app.js",
        "dashboard/static/app.css",
        "evidence/public_dashboard/dashboard_evidence.json",
        "evidence/cost_impact/cost_impact_summary.json",
        "sample_data/sample_meter_readings.csv",
        "sample_data/edge_demo_readings.csv",
        "requirements-dashboard.lock.txt",
        "requirements.lock.txt",
        "requirements-dev.lock.txt",
        "requirements-training.lock.txt",
        "models/public_demo/live_forecaster.json",
        "scripts/setup_and_launch.py",
        "scripts/security_scan.py",
        "scripts/repository_audit.py",
        "START_AI4I_EMS.bat",
        "START_EDGE_DEMO.bat",
        "RUN_STAGE4_COST_MODEL.bat",
        "TRAIN_PRIVATE_LIVE_MODEL.bat",
        "TEAM_SETUP_AND_RUN_INSTRUCTIONS.txt",
        "FINAL_DEMO_INSTRUCTIONS.txt",
        ".env.example",
    ]
    missing = [relative for relative in required if not (ROOT / relative).is_file()]
    assert missing == []


def test_private_and_local_content_is_not_present() -> None:
    forbidden = [
        ".venv",
        "private_data",
        "raw_data",
        "private_models",
        "release",
        "ci",
        "proposal",
        "screenshots",
        "env.example",
    ]
    assert [item for item in forbidden if (ROOT / item).exists()] == []
    assert not any(ROOT.glob("**/*DATA*UZ*ENERGY*.zip"))


def test_obsolete_executable_launchers_are_not_present() -> None:
    assert not any(ROOT.glob("**/AI4I_EMS_Setup_and_Launch.exe"))
