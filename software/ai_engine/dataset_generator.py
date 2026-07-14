from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import pi, sin, sqrt
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FacilityProfile:
    facility_id: str
    facility_name: str
    sector: str
    base_kw: float
    nominal_pf: float
    load_type: str


FACILITIES = [
    FacilityProfile("UZ_CK_NC1", "Central Kitchens NC1", "Catering and Hostels", 95, 0.91, "kitchen"),
    FacilityProfile("UZ_CK_NC2", "Central Kitchens NC2", "Catering and Hostels", 88, 0.90, "kitchen"),
    FacilityProfile("UZ_CK_NC3", "Central Kitchens NC3", "Catering and Hostels", 72, 0.92, "kitchen"),
    FacilityProfile("UZ_CK_NC4", "Central Kitchens NC4", "Catering and Hostels", 65, 0.92, "kitchen"),
    FacilityProfile("UZ_HOSTEL_A", "Hostel A", "Catering and Hostels", 75, 0.95, "hostel"),
    FacilityProfile("UZ_HOSTEL_B", "Hostel B", "Catering and Hostels", 68, 0.95, "hostel"),
    FacilityProfile("UZ_SCR", "Senior Common Room", "Catering and Hostels", 52, 0.94, "hostel"),
    FacilityProfile("UZ_SU", "Students Union", "Catering and Hostels", 46, 0.94, "mixed"),
    FacilityProfile("UZ_FEBE", "Engineering and Built Environment", "Academics and Research", 80, 0.93, "academic"),
    FacilityProfile("UZ_AGRIC", "Agriculture", "Academics and Research", 62, 0.92, "academic"),
    FacilityProfile("UZ_VET", "Veterinary Science", "Academics and Research", 58, 0.86, "lab"),
    FacilityProfile("UZ_ICT", "ICT and Mathematics", "Academics and Research", 70, 0.94, "ict"),
    FacilityProfile("UZ_BIOSCI", "Biological Sciences", "Academics and Research", 64, 0.91, "lab"),
    FacilityProfile("UZ_LIBRARY", "Main Library", "Library", 85, 0.95, "library"),
    FacilityProfile("UZ_ADMIN", "Administration Block", "Administration", 38, 0.96, "admin"),
    FacilityProfile("UZ_MAINT", "Maintenance Workshops", "Administration", 42, 0.89, "workshop"),
    FacilityProfile("UZ_STAFF_RES", "Staff Residences", "Staff Residence", 44, 0.96, "residential"),
    FacilityProfile("UZ_PUMP", "Water Pump House", "Utilities", 30, 0.84, "pump"),
    FacilityProfile("UZ_SPORTS", "Sports Facilities", "Support Services", 25, 0.94, "mixed"),
    FacilityProfile("UZ_MED", "Medical Centre", "Support Services", 35, 0.94, "medical"),
    FacilityProfile("UZ_LAB_A", "Research Laboratory A", "Academics and Research", 55, 0.88, "lab"),
    FacilityProfile("UZ_SECURITY", "Security and Gatehouses", "Support Services", 18, 0.96, "baseload"),
]


def academic_status(ts: pd.Timestamp) -> str:
    month = ts.month
    day = ts.day
    if month in (12, 1):
        return "vacation"
    if month == 11 or (month == 4 and day >= 10):
        return "exam"
    if month in (9, 10, 2, 3, 4):
        return "active_semester"
    return "recess"


def tariff_period(ts: pd.Timestamp) -> str:
    hour = ts.hour + ts.minute / 60
    if 7 <= hour < 10 or 18 <= hour < 21:
        return "peak"
    if hour >= 22 or hour < 5:
        return "offpeak"
    return "standard"


def occupancy_factor(ts: pd.Timestamp, profile: FacilityProfile) -> float:
    status = academic_status(ts)
    hour = ts.hour + ts.minute / 60
    weekend = ts.dayofweek >= 5
    base = {"vacation": 0.35, "recess": 0.55, "active_semester": 0.85, "exam": 0.95}[status]
    if weekend and profile.load_type in {"academic", "lab", "admin", "workshop"}:
        base *= 0.45
    if profile.load_type == "library" and status == "exam":
        base *= 1.15
    if profile.load_type == "hostel" and status != "vacation":
        base *= 1.05
    if 0 <= hour < 5 and profile.load_type not in {"hostel", "residential", "baseload", "ict"}:
        base *= 0.55
    return float(np.clip(base, 0.1, 1.25))


def schedule_multiplier(ts: pd.Timestamp, profile: FacilityProfile) -> tuple[float, str]:
    hour = ts.hour + ts.minute / 60
    status = academic_status(ts)
    event = "normal"
    mult = 1.0

    if profile.load_type == "kitchen":
        if 5 <= hour < 8:
            mult += 1.6
            event = "kitchen_breakfast_peak"
        elif 10 <= hour < 14:
            mult += 1.25
            event = "kitchen_lunch_peak"
        elif 16 <= hour < 19:
            mult += 1.45
            event = "kitchen_dinner_peak"
        elif 0 <= hour < 4:
            mult += 0.15
            event = "kitchen_refrigeration_baseload"
    elif profile.load_type == "hostel":
        if 5.5 <= hour < 8.5:
            mult += 0.75
            event = "hostel_morning_peak"
        elif 18 <= hour < 23:
            mult += 1.05
            event = "evening_residential_peak"
        elif 0 <= hour < 5:
            mult += 0.35
    elif profile.load_type in {"academic", "lab", "workshop"}:
        if 8 <= hour < 17 and ts.dayofweek < 5 and status != "vacation":
            mult += 0.9
            event = "daytime_academic_peak"
        if profile.load_type == "lab" and 10 <= hour < 15 and status == "active_semester":
            mult += 0.45
            event = "lab_session_peak"
    elif profile.load_type == "library":
        if 8 <= hour < 22:
            mult += 0.75
            event = "library_daytime_peak"
        if status == "exam" and 18 <= hour < 23:
            mult += 0.65
            event = "library_exam_peak"
    elif profile.load_type == "admin":
        if 8 <= hour < 17 and ts.dayofweek < 5:
            mult += 0.8
            event = "office_hours_peak"
    elif profile.load_type == "pump":
        if int(hour * 2) % 4 == 0:
            mult += 1.8
            event = "pump_cycling"
    elif profile.load_type == "ict":
        if 8 <= hour < 20:
            mult += 0.55
            event = "ict_daytime_peak"
        else:
            mult += 0.25
    elif profile.load_type == "baseload":
        mult += 0.2

    if status == "vacation" and profile.load_type in {"kitchen", "academic", "library", "lab"}:
        mult *= 0.55
        event = "vacation_low_load"

    return mult, event


def weather_temperature(ts: pd.Timestamp, rng: np.random.Generator) -> float:
    day_angle = 2 * pi * (ts.dayofyear / 365.0)
    hour_angle = 2 * pi * ((ts.hour + ts.minute / 60) / 24.0)
    seasonal = 23 + 5 * sin(day_angle - 0.6)
    daily = 4 * sin(hour_angle - 1.2)
    return float(seasonal + daily + rng.normal(0, 0.8))


def apply_event_variation(
    ts: pd.Timestamp,
    profile: FacilityProfile,
    kw: float,
    pf: float,
    event: str,
    rng: np.random.Generator,
) -> tuple[float, float, str, bool]:
    anomaly = False
    hour = ts.hour + ts.minute / 60

    if profile.load_type == "kitchen" and 0 <= hour < 4 and rng.random() < 0.006:
        kw *= rng.uniform(1.8, 2.7)
        event = "refrigeration_fault"
        anomaly = True

    if profile.load_type in {"academic", "lab", "workshop"} and 19 <= hour < 23 and rng.random() < 0.004:
        kw *= rng.uniform(1.6, 2.4)
        event = "equipment_left_on_after_hours"
        anomaly = True

    if profile.facility_id in {"UZ_VET", "UZ_PUMP", "UZ_MAINT", "UZ_LAB_A"} and rng.random() < 0.018:
        pf = min(pf, rng.uniform(0.68, 0.82))
        event = "power_factor_issue"
        anomaly = True

    if rng.random() < 0.0015:
        kw *= rng.uniform(0.0, 0.08)
        event = "meter_dropout"
        anomaly = True

    if tariff_period(ts) == "standard" and 10 <= hour < 11 and rng.random() < 0.006:
        kw *= rng.uniform(1.25, 1.65)
        event = "rebound_after_load_shift"
        anomaly = True

    return kw, pf, event, anomaly


def generate_synthetic_uz_dataset(
    start: str = "2025-09-01",
    days: int = 244,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range(start=start, periods=days * 48, freq="30min")
    rows: list[dict[str, object]] = []

    for ts in timestamps:
        temp_c = weather_temperature(ts, rng)
        for profile in FACILITIES:
            occ = occupancy_factor(ts, profile)
            mult, event = schedule_multiplier(ts, profile)
            weather_mult = 1.0 + max(temp_c - 26, 0) * 0.018
            noise = rng.normal(1.0, 0.055)
            kw = max(profile.base_kw * occ * mult * weather_mult * noise, 1.0)
            pf = float(np.clip(profile.nominal_pf + rng.normal(0, 0.018), 0.72, 0.99))
            kw, pf, event, anomaly = apply_event_variation(ts, profile, kw, pf, event, rng)
            kva = kw / pf
            kvar = sqrt(max(kva**2 - kw**2, 0.0))
            voltage = float(np.clip(rng.normal(400, 7.5), 360, 430))
            current = kva * 1000 / (sqrt(3) * voltage)

            rows.append(
                {
                    "timestamp": ts,
                    "facility_id": profile.facility_id,
                    "facility_name": profile.facility_name,
                    "sector": profile.sector,
                    "load_type": profile.load_type,
                    "academic_status": academic_status(ts),
                    "tariff_period": tariff_period(ts),
                    "occupancy_proxy": round(occ, 3),
                    "weather_temp_c": round(temp_c, 2),
                    "avg_kw": round(kw, 3),
                    "kwh": round(kw * 0.5, 3),
                    "kva": round(kva, 3),
                    "kvarh": round(kvar * 0.5, 3),
                    "power_factor": round(pf, 3),
                    "voltage_v": round(voltage, 2),
                    "current_a": round(current, 2),
                    "event_type": event,
                    "is_anomaly": anomaly,
                    "quality_flag": "estimated" if event == "meter_dropout" else "ok",
                }
            )

    data = pd.DataFrame(rows).sort_values(["facility_id", "timestamp"]).reset_index(drop=True)
    data["kva_p85"] = data.groupby("facility_id")["kva"].transform(lambda s: s.quantile(0.85))
    data["kva_p95"] = data.groupby("facility_id")["kva"].transform(lambda s: s.quantile(0.95))
    data["peak_risk"] = np.where(
        data["kva"] >= data["kva_p95"],
        "high",
        np.where(data["kva"] >= data["kva_p85"], "medium", "low"),
    )
    data = data.drop(columns=["kva_p85", "kva_p95"])
    data["next_interval_kva"] = data.groupby("facility_id")["kva"].shift(-1)
    return data.dropna(subset=["next_interval_kva"]).reset_index(drop=True)


def save_synthetic_dataset(path: str | Path, days: int = 244, seed: int = 42) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = generate_synthetic_uz_dataset(days=days, seed=seed)
    data.to_csv(output, index=False)
    return output


if __name__ == "__main__":
    save_synthetic_dataset("software/data/generated/uz_synthetic_ems_dataset.csv")
    print("Saved software/data/generated/uz_synthetic_ems_dataset.csv")
