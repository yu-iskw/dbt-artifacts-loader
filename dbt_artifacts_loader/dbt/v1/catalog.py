# generated by datamodel-codegen:
#   filename:  catalog.json
#   timestamp: 2021-09-28T11:58:25+00:00

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Union

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel
from pydantic import Extra, Field


class CatalogMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/catalog/v1.json'
    dbt_version: Optional[str] = '0.19.0'
    generated_at: Optional[datetime] = '2021-02-10T04:42:33.680487Z'
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = {}


class TableMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    type: str
    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    comment: Optional[Optional[str]] = None
    owner: Optional[Optional[str]] = None


class ColumnMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    type: str
    comment: Optional[Optional[str]] = None
    index: int
    name: str


class StatsItem(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    id: str
    label: str
    value: Optional[Optional[Union[bool, str, float]]] = None
    description: Optional[Optional[str]] = None
    include: bool


class CatalogTable(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    metadata: TableMetadata
    columns: Dict[str, ColumnMetadata]
    stats: Dict[str, StatsItem]
    unique_id: Optional[Optional[str]] = None


class Catalog(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    metadata: CatalogMetadata
    nodes: Dict[str, CatalogTable]
    sources: Dict[str, CatalogTable]
    errors: Optional[Optional[List[str]]] = None