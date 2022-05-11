# -*- coding: utf-8 -*-
"""Data Source Factory.

Helper function to create data source instance based on a given type.

Copyright 2020, Gradient Zero
All rights reserved
"""
from dq0.sdk.data import binary, clients, image, sql, text


data_source_classes = {
    'excel': binary.excel.Excel,
    'feather': binary.feather.Feather,
    'hdf5': binary.hdf5.HDF5,
    'odf': binary.odf.ODF,
    'orc': binary.orc.ORC,
    'parquet': binary.parquet.Parquet,
    'sas': binary.sas.SAS,
    'spss': binary.spss.SPSS,
    'stata': binary.stata.Stata,
    'elasticsearch': clients.elastic_search.ElasticSearch,
    'image': image.Image,
    'bigquery': sql.big_query.BigQuery,
    'drill': sql.drill.Drill,
    'mssql': sql.mssql.MSSQL,
    'mysql': sql.mysql.MySQL,
    'oracle': sql.oracle.Oracle,
    'postgresql': sql.postgresql.PostgreSQL,
    'redshift': sql.redshift.Redshift,
    'saphana': sql.sap_hana.SAPHana,
    'snowflake': sql.snowflake.Snowflake,
    'sqlite': sql.sqlite.SQLite,
    'csv': text.csv.CSV,
    'json': text.json.JSON
}


def create_from_meta(meta_database):
    """Returns a matching data source instance based on the given type
    or None if no data source class for this type was found.

    Args:
        type: the type of the data source class to create.
        *args: positional arguments for the specific data source constructor.

    Returns:
        initialized data source class.
    """
    type_name = meta_database.connector.type_name

    if not isinstance(type_name, str) or type_name == '':
        raise ValueError('type must be string!')

    type_name = type_name.lower()
    type_name = type_name.replace(' ', '')
    type_name = type_name.replace('-', '')
    type_name = type_name.replace('_', '')

    if type_name not in data_source_classes.keys():
        raise ValueError(f"type_name {type_name} not found in available types {data_source_classes.keys()}")

    data_class = data_source_classes[type_name]

    return data_class(meta_database)
