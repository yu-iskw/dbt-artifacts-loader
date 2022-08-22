{% macro get_dbt_minor_version(version) %}
  {% set re = modules.re %}
  {% set pattern = '[\.][^\.]+$' %}
  {% set dbt_minor_version = re.sub(pattern, '', version) %}
  {{ return(dbt_minor_version) }}
{% endmacro %}

{% macro test_get_dbt_minor_version() %}
  {% set result = get_dbt_minor_version("1.0.3") %}
  {% if result != "1.0" %}
    {{ exceptions.raise_compiler_error("Expected 1.0, but " ~ result) }}
  {% endif %}

  {% set result = get_dbt_minor_version("1.1.0") %}
  {% if result != "1.1" %}
    {{ exceptions.raise_compiler_error("Expected 1.1, but " ~ result) }}
  {% endif %}

  {% set result = get_dbt_minor_version("1.1.1") %}
  {% if result != "1.1" %}
    {{ exceptions.raise_compiler_error("Expected 1.1, but " ~ result) }}
  {% endif %}

  {% set result = get_dbt_minor_version("1.2.0-rc1") %}
  {% if result != "1.2" %}
    {{ exceptions.raise_compiler_error("Expected 1.2, but " ~ result) }}
  {% endif %}
{% endmacro %}
