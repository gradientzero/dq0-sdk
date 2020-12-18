# -*- coding: utf-8 -*-
"""Data Source Metadata information

Attributes and read / write functions for metadata structures.

Copyright 2020, Gradient Zero
All rights reserved
"""

import copy
import os

import yaml


class Metadata:
    """Metadata class.

    Describes a data source via metadata information. See README.md for details.

    Attributes:
        name: parsed name property.
        description: parsed description property
        connection: data source connection URI
        type: parsed type propertey.
        schema:  name of the database
        privacy_budget: parsed privacy budget property.
        privacy_budget_interval_days: parsed privacy budget reset interval in days.
        synth_allowed: true to allow synthesized data for exploration
        privacy_level: 0, 1, 2 in ascending order of privacy protection (default is 2).
        tables: parsed database metadata.
    """

    def __init__(self, filename=None, yaml=None):
        """Create a new Metadata instance

        Args:
            filename: if given try and load metadata from file
            yaml: if given try and load metadata from string
        """
        self.name = None
        self.description = None
        self.connection = None
        self.type = None
        self.schemas = None
        self.tables = None
        self.privacy_budget = None
        self.privacy_budget_interval_days = None
        self.synth_allowed = False
        self.privacy_level = 2
        if filename is not None:
            self.read_from_yaml_file(filename)
        elif yaml is not None:
            self.read_from_yaml(yaml)

    def read_from_yaml_file(self, filename):
        """Reads metadata from the given yaml file.

        Args:
            filename: the path to the yaml file.
        """
        # check if file exists in current directory
        if not os.path.isfile(filename):
            raise FileNotFoundError('Could not find {}'.format(filename))

        with open(filename) as f:
            self.read_from_yaml(f)

    def read_from_yaml(self, yaml_input):
        """Reads metadata from the given yaml input.

        Args:
            yaml_input: open yaml file stream or yaml string.
        """
        meta = yaml.load(yaml_input, Loader=yaml.FullLoader)

        self.name = meta["name"] if "name" in meta else None
        self.description = meta["description"] if "description" in meta else None
        self.connection = meta["connection"] if "connection" in meta else None
        self.type = meta["type"] if "type" in meta else None
        self.schemas = {}
        self.privacy_budget = int(meta["privacy_budget"]) if "privacy_budget" in meta else None
        self.privacy_budget_interval_days = int(meta["privacy_budget_interval_days"]) if "privacy_budget_interval_days" in meta else None
        self.synth_allowed = bool(meta["synth_allowed"]) if "synth_allowed" in meta else False
        self.privacy_level = int(meta["privacy_level"]) if "privacy_level" in meta else 2

        for key in meta.keys():
            if key not in self.__dict__:
                self.schemas[key] = {}
                for table in meta[key].keys():
                    self.schemas[key][table] = Table.from_meta(table, meta[key][table])

    def to_dict(self, sm=False):  # noqa: C901
        """Returns a dict representation of this class.

        Args:
            sm: True to return the dict with the non-smartnoise properties stripped.

        Returns:
            Metadata as python dictionary.
        """
        meta = {}
        if not sm:
            if self.name is not None:
                meta["name"] = self.name
            if self.description is not None:
                meta["description"] = self.description
            if self.connection is not None:
                meta["connection"] = self.connection
            if self.type is not None:
                meta["type"] = self.type
        if self.schemas is not None and len(self.schemas) > 0:
            for schema in self.schemas.keys():
                meta[schema] = {}
                for table in self.schemas[schema].keys():
                    meta[schema][table] = self.schemas[schema][table].to_dict(sm=sm)
        if not sm:
            if self.privacy_budget is not None:
                meta["privacy_budget"] = self.privacy_budget
            if self.privacy_budget_interval_days is not None:
                meta["privacy_budget_interval_days"] = self.privacy_budget_interval_days
            if self.synth_allowed is not None:
                meta["synth_allowed"] = self.synth_allowed
            if self.privacy_level is not None:
                meta["privacy_level"] = self.privacy_level
        if sm:
            name = self.name if self.name is not None else 'Collection'
            meta = {name: meta}
        return meta

    def to_dict_sm(self):
        """Returns a dict representation of this metadata in smartnoise format."""
        return self.to_dict(sm=True)

    def combine_with(self, metadata):
        """Combines two metadata instances.
        Adds the first schema of the given metadata object and all of its tables to
        this metadata object.

        Returns:
            The combined metadata object (self)
        """
        if metadata is None or not isinstance(metadata, Metadata):
            raise ValueError('you need to pass at a valid Metadata object')
        for schema in metadata.schemas.keys():
            if schema not in self.schemas.keys():
                # different databases, just add it
                self.schemas[schema] = copy.deepcopy(metadata.schemas[schema])
            else:
                # same schema, combine tables
                for table in metadata.schemas[schema].keys():
                    self.schemas[schema][table] = copy.deepcopy(metadata.schemas[schema][table])
        return self

    def to_yaml_file(self, filename, sm=False):
        """Writes metadata to a yaml file at the given path.

        Args:
            filename: the path to the yaml file.
            sm: True to return the dict with the non-smartnoise properties stripped.
        """
        meta = self.to_dict(sm=sm)
        with open(filename, 'w') as outfile:
            yaml.dump(meta, outfile)

    def to_yaml(self, sm=False):
        """Writes metadata to a yaml string.

        Args:
            sm: True to return the dict with the non-smartnoise properties stripped.

        Returns:
            metadata as yaml string
        """
        meta = self.to_dict(sm=sm)
        return yaml.dump(meta)


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
            tau=None,
            columns=None):
        """Create a new table object.

        Args:
            name: the name of the table
            tau: tau value for privacy thresholding
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
        self.tau = tau
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
        tau = int(meta.pop("tau")) if 'tau' in meta else None
        columns = {}
        for column in meta.keys():
            columns[column] = Column.from_meta(column, meta[column])
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
            tau=tau,
            columns=columns
        )

    def to_dict(self, sm=False):  # noqa: C901
        """Returns a dict representation of this class."""
        meta = {}
        if not sm:
            if self.tau is not None:
                meta["tau"] = self.tau
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
            meta[column] = self.columns[column].to_dict(sm=sm)
        return meta


class Column():
    """Column represents a table column definition inside the metadata."""
    def __init__(
            self,
            name,
            _type='',
            bounded=None,
            lower=None,
            upper=None,
            use_auto_bounds=False,
            auto_bounds_prob=0.9,
            auto_lower=None,
            auto_upper=None,
            cardinality=0,
            allowed_values=None,
            private_id=False,
            selectable=False,
            mask=None):
        """Create a new table object.

        Args:
            name: the name of the table
            columns: columns of the table
        """
        self.name = name
        self.type = _type
        self.bounded = bounded
        self.lower = lower
        self.upper = upper
        self.use_auto_bounds = use_auto_bounds
        self.auto_bounds_prob = auto_bounds_prob
        self.auto_lower = auto_lower
        self.auto_upper = auto_upper
        self.cardinality = cardinality
        self.allowed_values = allowed_values
        self.private_id = private_id
        self.selectable = selectable
        self.mask = mask

    @staticmethod
    def from_meta(column, meta):
        """Create a column instance from the meta yaml part."""
        _type = meta["type"] if "type" in meta else None
        bounded = None
        lower = None
        upper = None
        auto_lower = None
        auto_upper = None
        cardinality = 0
        allowed_values = None
        mask = None
        bounded = bool(meta["bounded"]) if "bounded" in meta else False
        use_auto_bounds = bool(meta["use_auto_bounds"]) if "use_auto_bounds" in meta else False
        auto_bounds_prob = float(meta["auto_bounds_prob"]) if "auto_bounds_prob" in meta else None
        if _type == "boolean":
            pass
        elif _type == "datetime":
            pass
        elif _type == "int":
            lower = int(meta["lower"]) if "lower" in meta else None
            upper = int(meta["upper"]) if "upper" in meta else None
            auto_lower = int(meta["auto_lower"]) if "auto_lower" in meta else None
            auto_upper = int(meta["auto_upper"]) if "auto_upper" in meta else None
        elif _type == "float":
            lower = float(meta["lower"]) if "lower" in meta else None
            upper = float(meta["upper"]) if "upper" in meta else None
            auto_lower = float(meta["auto_lower"]) if "auto_lower" in meta else None
            auto_upper = float(meta["auto_upper"]) if "auto_upper" in meta else None
        elif _type == "string":
            cardinality = int(meta["cardinality"]) if "cardinality" in meta else 0
            allowed_values = meta["allowed_values"] if "allowed_values" in meta else None
            mask = meta["mask"] if "mask" in meta else None
        else:
            raise ValueError("Unknown column type {} for column {}".format(_type, column))
        private_id = bool(meta["private_id"]) if "private_id" in meta else False
        selectable = bool(meta["selectable"]) if "selectable" in meta else False
        return Column(
            column,
            _type=_type,
            bounded=bounded,
            lower=lower,
            upper=upper,
            use_auto_bounds=use_auto_bounds,
            auto_bounds_prob=auto_bounds_prob,
            auto_lower=auto_lower,
            auto_upper=auto_upper,
            cardinality=cardinality,
            allowed_values=allowed_values,
            private_id=private_id,
            selectable=selectable,
            mask=mask
        )

    def to_dict(self, sm=False):  # noqa: C901
        """Returns a dict representation of this class."""
        meta = {}
        if self.type is not None:
            meta["type"] = self.type
        if self.bounded is not None:
            meta["bounded"] = self.bounded
        if self.lower is not None:
            meta["lower"] = self.lower
        if self.upper is not None:
            meta["upper"] = self.upper
        if self.private_id is not None:
            meta["private_id"] = self.private_id
        if not sm:
            if self.use_auto_bounds is not None:
                meta["use_auto_bounds"] = self.use_auto_bounds
            if self.auto_bounds_prob is not None:
                meta["auto_bounds_prob"] = self.auto_bounds_prob
            if self.auto_lower is not None:
                meta["auto_lower"] = self.auto_lower
            if self.auto_upper is not None:
                meta["auto_upper"] = self.auto_upper
            if self.cardinality is not None:
                meta["cardinality"] = self.cardinality
            if self.allowed_values is not None:
                meta["allowed_values"] = self.allowed_values
            if self.selectable is not None:
                meta["selectable"] = self.selectable
            if self.mask is not None:
                meta["mask"] = self.mask
        return meta
