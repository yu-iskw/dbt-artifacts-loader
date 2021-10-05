# generated by datamodel-codegen:
#   filename:  run-results.json
#   timestamp: 2021-09-28T11:58:29+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel
from pydantic import Extra


class BaseArtifactMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: str
    dbt_version: Optional[str] = '0.20.0rc1'
    generated_at: Optional[datetime] = '2021-06-07T14:49:01.097134Z'
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = {}


class Status(Enum):
    success = 'success'
    error = 'error'
    skipped = 'skipped'


class Status1(Enum):
    pass_ = 'pass'
    error = 'error'
    fail = 'fail'
    warn = 'warn'


class Status2(Enum):
    pass_ = 'pass'
    warn = 'warn'
    error = 'error'
    runtime_error = 'runtime error'


class TimingInfo(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    started_at: Optional[Optional[datetime]] = None
    completed_at: Optional[Optional[datetime]] = None


class RunResultOutput(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    status: Union[Status, Status1, Status2]
    timing: List[TimingInfo]
    thread_id: str
    execution_time: float
    adapter_response: Dict[str, Any]
    message: Optional[Optional[str]] = None
    failures: Optional[Optional[int]] = None
    unique_id: str


class RunResults(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    metadata: BaseArtifactMetadata
    results: List[RunResultOutput]
    elapsed_time: float
    args: Optional[Dict[str, Any]] = {}
