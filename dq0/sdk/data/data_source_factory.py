# -*- coding: utf-8 -*-
"""Data Source Factory.

Helper function to create data source instance based on a given type.

Copyright 2020, Gradient Zero
All rights reserved
"""
import dq0.sdk.data as data


data_source_classes = {
    'excel': data.binary.excel.Excel,
    'feather': data.binary.feather.Feather,
    'hdf5': data.binary.hdf5.HDF5,
    'odf': data.binary.odf.ODF,
    'orc': data.binary.orc.ORC,
    'parquet': data.binary.parquet.Parquet,
    'sas': data.binary.sas.SAS,
    'spss': data.binary.spss.SPSS,
    'stata': data.binary.stata.Stata,
    'image': data.image.Image,
    'bigquery': data.sql.big_query.BigQuery,
    'drill': data.sql.drill.Drill,
    'mssql': data.sql.mssql.MSSQL,
    'mysql': data.sql.mysql.MySQL,
    'oracle': data.sql.oracle.Oracle,
    'postgresql': data.sql.postgresql.PostgreSQL,
    'redshift': data.sql.redshift.Redshift,
    'saphana': data.sql.sap_hana.SAPHana,
    'snowflake': data.sql.snowflake.Snowflake,
    'sqlite': data.sql.sqlite.SQLite,
    'csv': data.text.csv.CSV,
    'json': data.text.json.JSON
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
