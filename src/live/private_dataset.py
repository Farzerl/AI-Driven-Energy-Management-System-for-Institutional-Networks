from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path, PurePosixPath

import pandas as pd


def _normalise(name: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()


def _find_header_row(workbook: pd.ExcelFile, sheet_name: str) -> int:
    preview = workbook.parse(sheet_name=sheet_name, header=None, nrows=20)
    for index, row in preview.iterrows():
        labels = [_normalise(value) for value in row.tolist()]
        if any("date time" in label for label in labels) and any(
            "demand kva" in label for label in labels
        ):
            return int(index)
    raise ValueError(f"Could not locate the meter header row in sheet {sheet_name!r}")


def _column(columns: list[object], *terms: str) -> object | None:
    normalised = {_normalise(column): column for column in columns}
    for label, original in normalised.items():
        if all(term in label for term in terms):
            return original
    return None


def _read_excel(payload: bytes, filename: str, alias: str) -> pd.DataFrame:
    # Keep the workbook inside an explicit context manager so openpyxl releases
    # every handle before this function returns. Reading from memory also avoids
    # Windows locking extracted private XLSX files during temporary-folder cleanup.
    with io.BytesIO(payload) as stream:
        with pd.ExcelFile(stream, engine="openpyxl") as workbook:
            sheet = "Summed" if "Summed" in workbook.sheet_names else workbook.sheet_names[0]
            header = _find_header_row(workbook, sheet)
            data = workbook.parse(sheet_name=sheet, header=header)

    columns = data.columns.tolist()
    timestamp_col = _column(columns, "date", "time")
    kva_col = _column(columns, "demand", "kva")
    kwh_col = _column(columns, "consumption", "kwh")
    pf_col = _column(columns, "power", "factor")
    if timestamp_col is None or kva_col is None:
        raise ValueError(
            f"Required timestamp or Demand (kVA) column missing in {filename}"
        )

    timestamp = pd.to_datetime(
        data[timestamp_col].astype(str).str.strip(),
        format="%m/%d/%Y, %H:%M:%S",
        errors="coerce",
    )
    timestamp = timestamp.dt.tz_localize(
        "Africa/Harare",
        nonexistent="shift_forward",
        ambiguous="NaT",
    )
    kva = pd.to_numeric(data[kva_col], errors="coerce")
    kwh = (
        pd.to_numeric(data[kwh_col], errors="coerce")
        if kwh_col is not None
        else kva * 0.5
    )
    pf = (
        pd.to_numeric(data[pf_col], errors="coerce")
        if pf_col is not None
        else 0.9
    )
    return pd.DataFrame(
        {
            "timestamp": timestamp,
            "facility_id": alias,
            "kva": kva,
            "kwh": kwh,
            "power_factor": pf,
        }
    )


def _read_csv(payload: bytes, filename: str, alias: str) -> pd.DataFrame:
    with io.BytesIO(payload) as stream:
        data = pd.read_csv(stream)

    columns = data.columns.tolist()
    timestamp_col = _column(columns, "timestamp") or _column(columns, "date", "time")
    kva_col = _column(columns, "kva") or _column(columns, "demand", "kva")
    kwh_col = _column(columns, "kwh")
    pf_col = _column(columns, "power", "factor")
    if timestamp_col is None or kva_col is None:
        raise ValueError(f"Required timestamp or kVA column missing in {filename}")

    timestamp = pd.to_datetime(data[timestamp_col], errors="coerce", utc=True)
    kva = pd.to_numeric(data[kva_col], errors="coerce")
    return pd.DataFrame(
        {
            "timestamp": timestamp,
            "facility_id": alias,
            "kva": kva,
            "kwh": (
                pd.to_numeric(data[kwh_col], errors="coerce")
                if kwh_col is not None
                else kva * 0.5
            ),
            "power_factor": (
                pd.to_numeric(data[pf_col], errors="coerce")
                if pf_col is not None
                else 0.9
            ),
        }
    )


def load_private_archive(
    archive: Path,
    output_dir: Path,
) -> tuple[pd.DataFrame, dict[str, str]]:
    archive = Path(archive)
    if not archive.exists() or archive.suffix.lower() != ".zip":
        raise FileNotFoundError(f"Private dataset ZIP not found: {archive}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read each supported member directly from the ZIP. No raw workbook is
    # extracted to %TEMP%, so Windows cannot block cleanup and private source
    # files are not left behind after training.
    with zipfile.ZipFile(archive) as handle:
        members = sorted(
            [
                member
                for member in handle.infolist()
                if not member.is_dir()
                and PurePosixPath(member.filename).suffix.lower() in {".xlsx", ".csv"}
                and not PurePosixPath(member.filename).name.startswith("~$")
            ],
            key=lambda member: member.filename.lower(),
        )
        if not members:
            raise ValueError(
                "No XLSX or CSV meter files were found in the private dataset ZIP."
            )

        frames: list[pd.DataFrame] = []
        alias_map: dict[str, str] = {}
        for index, member in enumerate(members, start=1):
            alias = f"F{index:02d}"
            filename = PurePosixPath(member.filename).name
            alias_map[alias] = filename
            with handle.open(member, "r") as source:
                payload = source.read()

            suffix = PurePosixPath(member.filename).suffix.lower()
            if suffix == ".xlsx":
                frame = _read_excel(payload, filename, alias)
            else:
                frame = _read_csv(payload, filename, alias)
            frames.append(frame)

    data = pd.concat(frames, ignore_index=True)
    data = data.dropna(subset=["timestamp", "kva", "kwh", "power_factor"])
    data = data[
        (data["kva"] >= 0)
        & (data["kwh"] >= 0)
        & data["power_factor"].between(-1, 1)
    ]
    data = data.sort_values(["facility_id", "timestamp"]).drop_duplicates(
        subset=["facility_id", "timestamp"],
        keep="last",
    )

    # The private alias map remains in the ignored private workspace.
    pd.Series(alias_map).to_json(
        output_dir / "facility_alias_map.private.json",
        indent=2,
    )
    return data.reset_index(drop=True), alias_map
