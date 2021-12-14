# -*- coding: utf-8 -*-
"""Data Source Factory.

Helper function to create data source instance based on a given type.

Copyright 2020, Gradient Zero
All rights reserved
"""
from dq0.sdk.data import binary, image, sql, text


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


def create_from_type(type, *args):
    """Returns a matching data source instance based on the given type
    or None if no data source class for this type was found.

    Args:
        type: the type of the data source class to create.
        *args: positional arguments for the specific data source constructor.

    Returns:
        initialized data source class.
    """
    if not isinstance(type, str) or type == '':
        raise ValueError('type must be string!')

    type = type.lower()
    type = type.replace(' ', '')
    type = type.replace('-', '')
    type = type.replace('_', '')

    if type not in data_source_classes.keys():
        raise ValueError('type {} not found in available types {}'.format(type, ', '.join(data_source_classes.keys())))

    data_class = data_source_classes[type]

    return data_class(*args)
