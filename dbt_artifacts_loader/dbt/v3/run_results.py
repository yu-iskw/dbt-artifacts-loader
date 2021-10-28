# generated by datamodel-codegen:
#   filename:  run-results.json
#   timestamp: 2021-10-28T12:48:36+00:00

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
    dbt_version: Optional[str] = '0.21.0rc1'
    generated_at: Optional[datetime] = '2021-09-24T13:29:14.315088Z'
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
    skipped = 'skipped'


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


class FreshnessMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/sources/v2.json'
    dbt_version: Optional[str] = '0.21.0rc1'
    generated_at: Optional[datetime] = '2021-09-24T13:29:14.312598Z'
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = {}


class Status3(Enum):
    runtime_error = 'runtime error'


class SourceFreshnessRuntimeError(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    unique_id: str
    error: Optional[Optional[Union[str, int]]] = None
    status: Status3


class Status4(Enum):
    pass_ = 'pass'
    warn = 'warn'
    error = 'error'
    runtime_error = 'runtime error'


class Period(Enum):
    minute = 'minute'
    hour = 'hour'
    day = 'day'


class Time(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    count: int
    period: Period


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


class FreshnessThreshold(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    warn_after: Optional[Optional[Time]] = None
    error_after: Optional[Optional[Time]] = None
    filter: Optional[Optional[str]] = None


class RunResultsV3(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    metadata: BaseArtifactMetadata
    results: List[RunResultOutput]
    elapsed_time: float
    args: Optional[Dict[str, Any]] = {}


class SourceFreshnessOutput(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    unique_id: str
    max_loaded_at: datetime
    snapshotted_at: datetime
    max_loaded_at_time_ago_in_s: float
    status: Status4
    criteria: FreshnessThreshold
    adapter_response: Dict[str, Any]
    timing: List[TimingInfo]
    thread_id: str
    execution_time: float
