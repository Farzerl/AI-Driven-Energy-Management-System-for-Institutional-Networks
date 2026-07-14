from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class OperatorDecision(BaseModel):
    alert_id: str = Field(min_length=8, max_length=64)
    decision: Literal["confirm", "defer", "dismiss", "mute"]
    operator: str = Field(default="demo-operator", min_length=2, max_length=80)
    note: str = Field(default="", max_length=500)
    requested_reduction_kva: float | None = Field(default=None, ge=0)


class HealthResponse(BaseModel):
    status: str
    evidence_ready: bool
    operating_mode: str
    api_key_required: bool
    model_ready: bool = False
