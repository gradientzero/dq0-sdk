# -*- coding: utf-8 -*-
"""Data Source Metadata information

Attributes and read / write functions for metadata structures.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import yaml


class Metadata:
    """Metadata class.

    Describes a data source via metadata information. See README.md for details.

    Attributes:
        name: parsed name property.
        description: parsed description property
        type: parsed type propertey.
        privacy_budget: parsed privacy budget property.
        privacy_budget_interval_days: parsed privacy budget reset interval in days.
        tables: parsed database metadata.
    """

    def __init__(self, filename=None):
        """Create a new Metadata instance"""
        self.name = None
        self.description = None
        self.type = None
        self.tables = None
        self.privacy_budget = None
        self.privacy_budget_interval_days = None
        if filename is not None:
            self.read_from_yaml(filename)

    def read_from_yaml(self, filename):
        """Reads metadata from the given yaml file.

        Args:
            filename: the path to the yaml file.
        """
        # check if .meta file exists in current directory
        if not os.path.isfile(filename):
            raise FileNotFoundError('Could not find {}'.format(filename))

        with open(filename) as f:
            meta = yaml.load(f, Loader=yaml.FullLoader)

        self.name = meta["name"] if "name" in meta else None
        self.description = meta["description"] if "description" in meta else None
        self.type = meta["type"] if "type" in meta else None
        self.privacy_budget = int(meta["privacy_budget"]) if "privacy_budget" in meta else None
        self.privacy_budget_interval_days = int(meta["privacy_budget_interval_days"]) if "privacy_budget_interval_days" else None

        if "database" in meta:
            db = meta["database"]
            tables = []
            for table in db.keys():
                tables.append(Table.from_meta(table, db[table]))
            self.tables = tables

    def to_dict(self):
        """Returns a dict representation of this class."""
        meta = {}
        if self.name is not None:
            meta["name"] = self.name
        if self.description is not None:
            meta["description"] = self.description
        if self.type is not None:
            meta["type"] = self.type
        if self.tables is not None and len(self.tables) > 0:
            meta["database"] = {}
            for table in self.tables:
                meta["database"][table.name] = table.to_dict()
        if self.privacy_budget is not None:
            meta["privacy_budget"] = self.privacy_budget
        if self.privacy_budget_interval_days is not None:
            meta["privacy_budget_interval_days"] = self.privacy_budget_interval_days
        return meta

    def write_to_yaml(self, filename):
        """Writes metadata to a yaml file at the given path.

        Args:
            filename: the path to the yaml file.
        """
        meta = self.to_dict()
        with open(filename, 'w') as outfile:
            yaml.dump(meta, outfile)


class Table():
    """Table represents a table definition inside the metadata."""
    def __init__(
            self,
            name,
            row_privacy=False,
            rows=0,
            max_ids=1,
            sample_max_ids=True,
            use_dpsu=False,
            clamp_counts=False,
            clamp_columns=False,
            censor_dims=False,
            columns=None):
        """Create a new table object.

        Args:
            name: the name of the table
            columns: columns of the table
        """
        self.name = name
        self.row_privacy = row_privacy
        self.rows = rows
        self.max_ids = max_ids
        self.sample_max_ids = sample_max_ids
        self.use_dpsu = use_dpsu
        self.clamp_counts = clamp_counts
        self.clamp_columns = clamp_columns
        self.censor_dims = censor_dims
        self.columns = columns

    @staticmethod
    def from_meta(table, meta):
        """Create a table instance from the meta yaml part."""
        row_privacy = bool(meta.pop("row_privacy", False))
        rows = int(meta.pop("rows", 0))
        max_ids = int(meta.pop("max_ids", 1))
        sample_max_ids = bool(meta.pop("sample_max_ids", True))
        use_dpsu = bool(meta.pop("use_dpsu", False))
        clamp_counts = bool(meta.pop("clamp_counts", False))
        clamp_columns = bool(meta.pop("clamp_columns", True))
        censor_dims = bool(meta.pop("censor_dims", False))
        columns = []
        for column in meta.keys():
            columns.append(Column.from_meta(column, meta[column]))
        return Table(
            table,
            row_privacy=row_privacy,
            rows=rows,
            max_ids=max_ids,
            sample_max_ids=sample_max_ids,
            use_dpsu=use_dpsu,
            clamp_counts=clamp_counts,
            clamp_columns=clamp_columns,
            censor_dims=censor_dims,
            columns=columns
        )

    def to_dict(self):
        """Returns a dict representation of this class."""
        meta = {}
        if self.name is not None:
            meta["name"] = self.name
        if self.row_privacy is not None:
            meta["row_privacy"] = self.row_privacy
        if self.rows is not None:
            meta["rows"] = self.rows
        if self.max_ids is not None:
            meta["max_ids"] = self.max_ids
        if self.sample_max_ids is not None:
            meta["sample_max_ids"] = self.sample_max_ids
        if self.use_dpsu is not None:
            meta["use_dpsu"] = self.use_dpsu
        if self.clamp_counts is not None:
            meta["clamp_counts"] = self.clamp_counts
        if self.clamp_columns is not None:
            meta["clamp_columns"] = self.clamp_columns
        if self.censor_dims is not None:
            meta["censor_dims"] = self.censor_dims
        for column in self.columns:
            meta[column.name] = column.to_dict()
        return meta


class Column():
    """Column represents a table column definition inside the metadata."""
    def __init__(self, name, _type='', lower=None, upper=None, cardinality=0, private_id=False, hide=False, mask=None):
        """Create a new table object.

        Args:
            name: the name of the table
            columns: columns of the table
        """
        self.name = name
        self.type = _type
        self.lower = lower
        self.upper = upper
        self.cardinality = cardinality
        self.private_id = private_id
        self.hide = hide
        self.mask = mask

    @staticmethod
    def from_meta(column, meta):
        """Create a column instance from the meta yaml part."""
        _type = meta["type"] if "type" in meta else None
        lower = None
        upper = None
        cardinality = 0
        if _type == "boolean":
            pass
        elif _type == "datetime":
            pass
        elif _type == "int":
            lower = int(meta["lower"]) if "lower" in meta else None
            upper = int(meta["upper"]) if "upper" in meta else None
        elif _type == "float":
            lower = float(meta["lower"]) if "lower" in meta else None
            upper = float(meta["upper"]) if "upper" in meta else None
        elif _type == "string":
            cardinality = int(meta["cardinality"]) if "cardinality" in meta else 0
        else:
            raise ValueError("Unknown column type for column {}".format(_type))
        private_id = bool(meta["private_id"]) if "private_id" in meta else False
        hide = bool(meta["hide"]) if "hide" in meta else False
        mask = meta["mask"] if "mask" in meta else None
        return Column(
            column,
            _type=_type,
            lower=lower,
            upper=upper,
            cardinality=cardinality,
            private_id=private_id,
            hide=hide,
            mask=mask
        )

    def to_dict(self):
        """Returns a dict representation of this class."""
        meta = {}
        if self.type is not None:
            meta["type"] = self.type
        if self.lower is not None:
            meta["lower"] = self.lower
        if self.upper is not None:
            meta["upper"] = self.upper
        if self.cardinality is not None:
            meta["cardinality"] = self.cardinality
        if self.private_id is not None:
            meta["private_id"] = self.private_id
        if self.hide is not None:
            meta["hide"] = self.hide
        if self.mask is not None:
            meta["mask"] = self.mask
        return meta
