# generated by datamodel-codegen:
#   filename:  manifest.json
#   timestamp: 2023-04-03T12:02:49+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Extra, Field, constr

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel


class ManifestMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[
        str
    ] = 'https://schemas.getdbt.com/dbt/manifest/v8.json'
    dbt_version: Optional[str] = '1.4.1'
    generated_at: Optional[datetime] = '2023-02-09T10:04:47.350768Z'
    invocation_id: Optional[Optional[str]] = 'f795bc66-f417-4007-af6e-f2e513d33790'
    env: Optional[Dict[str, str]] = {}
    project_id: Optional[Optional[str]] = Field(
        None, description='A unique identifier for the project'
    )
    user_id: Optional[
        Optional[
            constr(
                regex=r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
            )
        ]
    ] = Field(None, description='A unique identifier for the user')
    send_anonymous_usage_stats: Optional[Optional[bool]] = Field(
        None, description='Whether dbt is configured to send anonymous usage statistics'
    )
    adapter_type: Optional[Optional[str]] = Field(
        None, description='The type name of the adapter'
    )


class ResourceType(Enum):
    analysis = 'analysis'


class FileHash(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    checksum: str


class Hook(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    sql: str
    transaction: Optional[bool] = True
    index: Optional[Optional[int]] = None


class Docs(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    show: Optional[bool] = True
    node_color: Optional[Optional[str]] = None


class ColumnInfo(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    name: str
    description: Optional[str] = ''
    meta: Optional[Dict[str, Any]] = {}
    data_type: Optional[Optional[str]] = None
    quote: Optional[Optional[bool]] = None
    tags: Optional[List[str]] = []


class DependsOn(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    macros: Optional[List[str]] = []
    nodes: Optional[List[str]] = []


class InjectedCTE(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    id: str
    sql: str


class ResourceType1(Enum):
    test = 'test'


class TestConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True
    alias: Optional[Optional[str]] = None
    schema_: Optional[Optional[str]] = Field('dbt_test__audit', alias='schema')
    database: Optional[Optional[str]] = None
    tags: Optional[Union[List[str], str]] = []
    meta: Optional[Dict[str, Any]] = {}
    materialized: Optional[str] = 'test'
    severity: Optional[
        constr(regex=r'^([Ww][Aa][Rr][Nn]|[Ee][Rr][Rr][Oo][Rr])$')
    ] = 'ERROR'
    store_failures: Optional[Optional[bool]] = None
    where: Optional[Optional[str]] = None
    limit: Optional[Optional[int]] = None
    fail_calc: Optional[str] = 'count(*)'
    warn_if: Optional[str] = '!= 0'
    error_if: Optional[str] = '!= 0'


class ResourceType2(Enum):
    operation = 'operation'


class ResourceType3(Enum):
    model = 'model'


class ResourceType4(Enum):
    rpc = 'rpc'


class ResourceType5(Enum):
    sql_operation = 'sql operation'


class ResourceType6(Enum):
    test = 'test'


class TestMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    kwargs: Optional[Dict[str, Any]] = {}
    namespace: Optional[Optional[str]] = None


class ResourceType7(Enum):
    snapshot = 'snapshot'


class SnapshotConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True
    alias: Optional[Optional[str]] = None
    schema_: Optional[Optional[str]] = Field(None, alias='schema')
    database: Optional[Optional[str]] = None
    tags: Optional[Union[List[str], str]] = []
    meta: Optional[Dict[str, Any]] = {}
    materialized: Optional[str] = 'snapshot'
    incremental_strategy: Optional[Optional[str]] = None
    persist_docs: Optional[Dict[str, Any]] = {}
    post_hook: Optional[List[Hook]] = Field([], alias='post-hook')
    pre_hook: Optional[List[Hook]] = Field([], alias='pre-hook')
    quoting: Optional[Dict[str, Any]] = {}
    column_types: Optional[Dict[str, Any]] = {}
    full_refresh: Optional[Optional[bool]] = None
    unique_key: Optional[Optional[str]] = None
    on_schema_change: Optional[Optional[str]] = 'ignore'
    grants: Optional[Dict[str, Any]] = {}
    packages: Optional[List[str]] = []
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    strategy: Optional[Optional[str]] = None
    target_schema: Optional[Optional[str]] = None
    target_database: Optional[Optional[str]] = None
    updated_at: Optional[Optional[str]] = None
    check_cols: Optional[Optional[Union[str, List[str]]]] = None


class ResourceType8(Enum):
    seed = 'seed'


class SeedConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True
    alias: Optional[Optional[str]] = None
    schema_: Optional[Optional[str]] = Field(None, alias='schema')
    database: Optional[Optional[str]] = None
    tags: Optional[Union[List[str], str]] = []
    meta: Optional[Dict[str, Any]] = {}
    materialized: Optional[str] = 'seed'
    incremental_strategy: Optional[Optional[str]] = None
    persist_docs: Optional[Dict[str, Any]] = {}
    post_hook: Optional[List[Hook]] = Field([], alias='post-hook')
    pre_hook: Optional[List[Hook]] = Field([], alias='pre-hook')
    quoting: Optional[Dict[str, Any]] = {}
    column_types: Optional[Dict[str, Any]] = {}
    full_refresh: Optional[Optional[bool]] = None
    unique_key: Optional[Optional[Union[str, List[str]]]] = None
    on_schema_change: Optional[Optional[str]] = 'ignore'
    grants: Optional[Dict[str, Any]] = {}
    packages: Optional[List[str]] = []
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    quote_columns: Optional[Optional[bool]] = None


class MacroDependsOn(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    macros: Optional[List[str]] = []


class ResourceType9(Enum):
    source = 'source'


class Quoting(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[bool]] = None
    schema_: Optional[Optional[bool]] = Field(None, alias='schema')
    identifier: Optional[Optional[bool]] = None
    column: Optional[Optional[bool]] = None


class FreshnessMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/sources/v3.json'
    dbt_version: Optional[str] = '1.4.1'
    generated_at: Optional[datetime] = '2023-02-09T10:04:47.347023Z'
    invocation_id: Optional[Optional[str]] = 'f795bc66-f417-4007-af6e-f2e513d33790'
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


class PeriodEnum(Enum):
    minute = 'minute'
    hour = 'hour'
    day = 'day'


class Time(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    count: Optional[Optional[int]] = None
    period: Optional[Optional[PeriodEnum]] = None


class TimingInfo(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    started_at: Optional[Optional[datetime]] = None
    completed_at: Optional[Optional[datetime]] = None


class ExternalPartition(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    name: Optional[str] = ''
    description: Optional[str] = ''
    data_type: Optional[str] = ''
    meta: Optional[Dict[str, Any]] = {}


class SourceConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True


class ResourceType10(Enum):
    macro = 'macro'


class SupportedLanguage(Enum):
    python = 'python'
    sql = 'sql'


class MacroArgument(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    type: Optional[Optional[str]] = None
    description: Optional[str] = ''


class ResourceType11(Enum):
    doc = 'doc'


class Documentation(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    resource_type: ResourceType11
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    block_contents: str


class ResourceType12(Enum):
    exposure = 'exposure'


class Type(Enum):
    dashboard = 'dashboard'
    notebook = 'notebook'
    analysis = 'analysis'
    ml = 'ml'
    application = 'application'


class MaturityEnum(Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class ExposureOwner(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    email: str
    name: Optional[Optional[str]] = None


class ExposureConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True


class ResourceType13(Enum):
    metric = 'metric'


class MetricFilter(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    field: str
    operator: str
    value: str


class PeriodEnum1(Enum):
    day = 'day'
    week = 'week'
    month = 'month'
    year = 'year'


class MetricTime(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    count: Optional[Optional[int]] = None
    period: Optional[Optional[PeriodEnum1]] = None


class MetricConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True


class NodeConfig(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    enabled: Optional[bool] = True
    alias: Optional[Optional[str]] = None
    schema_: Optional[Optional[str]] = Field(None, alias='schema')
    database: Optional[Optional[str]] = None
    tags: Optional[Union[List[str], str]] = []
    meta: Optional[Dict[str, Any]] = {}
    materialized: Optional[str] = 'view'
    incremental_strategy: Optional[Optional[str]] = None
    persist_docs: Optional[Dict[str, Any]] = {}
    post_hook: Optional[List[Hook]] = Field([], alias='post-hook')
    pre_hook: Optional[List[Hook]] = Field([], alias='pre-hook')
    quoting: Optional[Dict[str, Any]] = {}
    column_types: Optional[Dict[str, Any]] = {}
    full_refresh: Optional[Optional[bool]] = None
    unique_key: Optional[Optional[Union[str, List[str]]]] = None
    on_schema_change: Optional[Optional[str]] = 'ignore'
    grants: Optional[Dict[str, Any]] = {}
    packages: Optional[List[str]] = []
    docs: Optional[Docs] = {'show': True, 'node_color': None}


class SingularTestNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType1
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[TestConfig] = {
        'enabled': True,
        'alias': None,
        'schema': 'dbt_test__audit',
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'test',
        'severity': 'ERROR',
        'store_failures': None,
        'where': None,
        'limit': None,
        'fail_calc': 'count(*)',
        'warn_if': '!= 0',
        'error_if': '!= 0',
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.355371
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []


class HookNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType2
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[NodeConfig] = {
        'enabled': True,
        'alias': None,
        'schema': None,
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'view',
        'incremental_strategy': None,
        'persist_docs': {},
        'quoting': {},
        'column_types': {},
        'full_refresh': None,
        'unique_key': None,
        'on_schema_change': 'ignore',
        'grants': {},
        'packages': [],
        'docs': {'show': True, 'node_color': None},
        'post-hook': [],
        'pre-hook': [],
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.356482
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []
    index: Optional[Optional[int]] = None


class ModelNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType3
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[NodeConfig] = {
        'enabled': True,
        'alias': None,
        'schema': None,
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'view',
        'incremental_strategy': None,
        'persist_docs': {},
        'quoting': {},
        'column_types': {},
        'full_refresh': None,
        'unique_key': None,
        'on_schema_change': 'ignore',
        'grants': {},
        'packages': [],
        'docs': {'show': True, 'node_color': None},
        'post-hook': [],
        'pre-hook': [],
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.357701
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []


class RPCNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType4
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[NodeConfig] = {
        'enabled': True,
        'alias': None,
        'schema': None,
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'view',
        'incremental_strategy': None,
        'persist_docs': {},
        'quoting': {},
        'column_types': {},
        'full_refresh': None,
        'unique_key': None,
        'on_schema_change': 'ignore',
        'grants': {},
        'packages': [],
        'docs': {'show': True, 'node_color': None},
        'post-hook': [],
        'pre-hook': [],
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.358761
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []


class SqlNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType5
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[NodeConfig] = {
        'enabled': True,
        'alias': None,
        'schema': None,
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'view',
        'incremental_strategy': None,
        'persist_docs': {},
        'quoting': {},
        'column_types': {},
        'full_refresh': None,
        'unique_key': None,
        'on_schema_change': 'ignore',
        'grants': {},
        'packages': [],
        'docs': {'show': True, 'node_color': None},
        'post-hook': [],
        'pre-hook': [],
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.359803
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []


class GenericTestNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    test_metadata: TestMetadata
    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType6
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[TestConfig] = {
        'enabled': True,
        'alias': None,
        'schema': 'dbt_test__audit',
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'test',
        'severity': 'ERROR',
        'store_failures': None,
        'where': None,
        'limit': None,
        'fail_calc': 'count(*)',
        'warn_if': '!= 0',
        'error_if': '!= 0',
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.361009
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []
    column_name: Optional[Optional[str]] = None
    file_key_name: Optional[Optional[str]] = None


class SnapshotNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType7
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: SnapshotConfig
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.364386
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []


class SeedNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType8
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[SeedConfig] = {
        'enabled': True,
        'alias': None,
        'schema': None,
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'seed',
        'incremental_strategy': None,
        'persist_docs': {},
        'quoting': {},
        'column_types': {},
        'full_refresh': None,
        'unique_key': None,
        'on_schema_change': 'ignore',
        'grants': {},
        'packages': [],
        'docs': {'show': True, 'node_color': None},
        'quote_columns': None,
        'post-hook': [],
        'pre-hook': [],
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.366245
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    root_path: Optional[Optional[str]] = None
    depends_on: Optional[MacroDependsOn] = {'macros': []}


class FreshnessThreshold(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    warn_after: Optional[Optional[Time]] = {'count': None, 'period': None}
    error_after: Optional[Optional[Time]] = {'count': None, 'period': None}
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
    timing: List[TimingInfo]
    thread_id: str
    execution_time: float


class ExternalTable(BaseBigQueryModel):
    class Config:
        extra = Extra.allow

    location: Optional[Optional[str]] = None
    file_format: Optional[Optional[str]] = None
    row_format: Optional[Optional[str]] = None
    tbl_properties: Optional[Optional[str]] = None
    partitions: Optional[Optional[Union[List[str], List[ExternalPartition]]]] = None


class Macro(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    resource_type: ResourceType10
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    macro_sql: str
    depends_on: Optional[MacroDependsOn] = {'macros': []}
    description: Optional[str] = ''
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    arguments: Optional[List[MacroArgument]] = []
    created_at: Optional[float] = 1675937087.368656
    supported_languages: Optional[Optional[List[SupportedLanguage]]] = None


class Exposure(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    resource_type: ResourceType12
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    type: Type
    owner: ExposureOwner
    description: Optional[str] = ''
    label: Optional[Optional[str]] = None
    maturity: Optional[Optional[MaturityEnum]] = None
    meta: Optional[Dict[str, Any]] = {}
    tags: Optional[List[str]] = []
    config: Optional[ExposureConfig] = {'enabled': True}
    unrendered_config: Optional[Dict[str, Any]] = {}
    url: Optional[Optional[str]] = None
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    created_at: Optional[float] = 1675937087.369866


class Metric(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    name: str
    resource_type: ResourceType13
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    description: str
    label: str
    calculation_method: str
    expression: str
    filters: List[MetricFilter]
    time_grains: List[str]
    dimensions: List[str]
    timestamp: Optional[Optional[str]] = None
    window: Optional[Optional[MetricTime]] = None
    model: Optional[Optional[str]] = None
    model_unique_id: Optional[Optional[str]] = None
    meta: Optional[Dict[str, Any]] = {}
    tags: Optional[List[str]] = []
    config: Optional[MetricConfig] = {'enabled': True}
    unrendered_config: Optional[Dict[str, Any]] = {}
    sources: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    refs: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    created_at: Optional[float] = 1675937087.371092


class AnalysisNode(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    alias: str
    checksum: FileHash
    config: Optional[NodeConfig] = {
        'enabled': True,
        'alias': None,
        'schema': None,
        'database': None,
        'tags': [],
        'meta': {},
        'materialized': 'view',
        'incremental_strategy': None,
        'persist_docs': {},
        'quoting': {},
        'column_types': {},
        'full_refresh': None,
        'unique_key': None,
        'on_schema_change': 'ignore',
        'grants': {},
        'packages': [],
        'docs': {'show': True, 'node_color': None},
        'post-hook': [],
        'pre-hook': [],
    }
    tags: Optional[List[str]] = []
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    docs: Optional[Docs] = {'show': True, 'node_color': None}
    patch_path: Optional[Optional[str]] = None
    build_path: Optional[Optional[str]] = None
    deferred: Optional[bool] = False
    unrendered_config: Optional[Dict[str, Any]] = {}
    created_at: Optional[float] = 1675937087.353436
    config_call_dict: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    raw_code: Optional[str] = ''
    language: Optional[str] = 'sql'
    refs: Optional[List[List[str]]] = []
    sources: Optional[List[List[str]]] = []
    metrics: Optional[List[List[str]]] = []
    depends_on: Optional[DependsOn] = {'macros': [], 'nodes': []}
    compiled_path: Optional[Optional[str]] = None
    compiled: Optional[bool] = False
    compiled_code: Optional[Optional[str]] = None
    extra_ctes_injected: Optional[bool] = False
    extra_ctes: Optional[List[InjectedCTE]] = []


class SourceDefinition(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    database: Optional[Optional[str]] = None
    schema_: str = Field(..., alias='schema')
    name: str
    resource_type: ResourceType9
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]
    source_name: str
    source_description: str
    loader: str
    identifier: str
    quoting: Optional[Quoting] = {
        'database': None,
        'schema': None,
        'identifier': None,
        'column': None,
    }
    loaded_at_field: Optional[Optional[str]] = None
    freshness: Optional[Optional[FreshnessThreshold]] = None
    external: Optional[Optional[ExternalTable]] = None
    description: Optional[str] = ''
    columns: Optional[Dict[str, ColumnInfo]] = {}
    meta: Optional[Dict[str, Any]] = {}
    source_meta: Optional[Dict[str, Any]] = {}
    tags: Optional[List[str]] = []
    config: Optional[SourceConfig] = {'enabled': True}
    patch_path: Optional[Optional[str]] = None
    unrendered_config: Optional[Dict[str, Any]] = {}
    relation_name: Optional[Optional[str]] = None
    created_at: Optional[float] = 1675937087.368067


class ManifestV8(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    # The loaded_at field was manually added.
    loaded_at: datetime = Field(default=datetime.utcnow(),
                                description="The loaded time by dbt-artifacts-loader")
    metadata: ManifestMetadata = Field(..., description='Metadata about the manifest')
    nodes: Dict[
        str,
        Union[
            AnalysisNode,
            SingularTestNode,
            HookNode,
            ModelNode,
            RPCNode,
            SqlNode,
            GenericTestNode,
            SnapshotNode,
            SeedNode,
        ],
    ] = Field(
        ..., description='The nodes defined in the dbt project and its dependencies'
    )
    sources: Dict[str, SourceDefinition] = Field(
        ..., description='The sources defined in the dbt project and its dependencies'
    )
    macros: Dict[str, Macro] = Field(
        ..., description='The macros defined in the dbt project and its dependencies'
    )
    docs: Dict[str, Documentation] = Field(
        ..., description='The docs defined in the dbt project and its dependencies'
    )
    exposures: Dict[str, Exposure] = Field(
        ..., description='The exposures defined in the dbt project and its dependencies'
    )
    metrics: Dict[str, Metric] = Field(
        ..., description='The metrics defined in the dbt project and its dependencies'
    )
    selectors: Dict[str, Any] = Field(
        ..., description='The selectors defined in selectors.yml'
    )
    disabled: Optional[
        Optional[
            Dict[
                str,
                List[
                    Union[
                        AnalysisNode,
                        SingularTestNode,
                        HookNode,
                        ModelNode,
                        RPCNode,
                        SqlNode,
                        GenericTestNode,
                        SnapshotNode,
                        SeedNode,
                        SourceDefinition,
                    ]
                ],
            ]
        ]
    ] = Field(None, description='A mapping of the disabled nodes in the target')
    parent_map: Optional[Optional[Dict[str, List[str]]]] = Field(
        None, description='A mapping from\xa0child nodes to their dependencies'
    )
    child_map: Optional[Optional[Dict[str, List[str]]]] = Field(
        None, description='A mapping from parent nodes to their dependents'
    )
