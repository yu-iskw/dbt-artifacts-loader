# generated by datamodel-codegen:
#   filename:  sources.json
#   timestamp: 2021-10-09T01:08:44+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel
from pydantic import Extra


class FreshnessMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/sources/v1.json'
    dbt_version: Optional[str] = '0.19.0'
    generated_at: Optional[datetime] = '2021-02-10T04:42:33.675309Z'
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = {}


class Status(Enum):
    runtime_error = 'runtime error'


class SourceFreshnessRuntimeError(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    unique_id: str
    error: Optional[Optional[Union[str, int]]] = None
    status: Status


class Status1(Enum):
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


class FreshnessThreshold(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    warn_after: Optional[Optional[Time]] = None
    error_after: Optional[Optional[Time]] = None
    filter: Optional[Optional[str]] = None


class SourceFreshnessOutput(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    unique_id: str
    max_loaded_at: datetime
    snapshotted_at: datetime
    max_loaded_at_time_ago_in_s: float
    status: Status1
    criteria: FreshnessThreshold
    adapter_response: Dict[str, Any]


class SourcesV1(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    metadata: FreshnessMetadata
    results: List[Union[SourceFreshnessRuntimeError, SourceFreshnessOutput]]
    elapsed_time: float
