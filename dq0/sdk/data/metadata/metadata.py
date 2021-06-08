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
        type: parsed type propertey.
        schemas: parsed schema metadata (see class Schema below)
        privacy_column: the unique privacy column for this data set
    """

    def __init__(self, filename=None, yaml=None):
        """Create a new Metadata instance

        Args:
            filename: if given try and load metadata from file
            yaml: if given try and load metadata from string
        """
        self.name = None
        self.description = None
        self.tags = None
        self.type = None
        self.schemas = None
        self.privacy_column = None
        self.metadata_is_public = False
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
        self.tags = meta["tags"] if "tags" in meta else None
        self.type = meta["type"] if "type" in meta else None
        self.schemas = {}
        self.privacy_column = meta["privacy_column"] if "privacy_column" in meta else None
        self.metadata_is_public = bool(meta.pop("metadata_is_public", False))
        # self.header = meta["header_columns"] if "header_columns" in meta else None

        for key in meta.keys():
            if key not in self.__dict__ and isinstance(meta[key], dict):
                self.schemas[key] = Schema.from_meta(key, meta[key])

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
            if self.tags is not None:
                meta["tags"] = self.tags
            if self.type is not None:
                meta["type"] = self.type
            if self.privacy_column is not None:
                meta["privacy_column"] = self.privacy_column
            meta["metadata_is_public"] = self.metadata_is_public

        if self.schemas is not None and len(self.schemas) > 0:
            for schema in self.schemas:
                meta[schema] = self.schemas[schema].to_dict(sm=sm)

        if sm:
            meta = {'Collection': meta}
            meta['engine'] = self.type

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
        schema_names = self.get_all_schema_names()
        for name, schema in metadata.schemas.items():
            if name not in schema_names:
                # different databases, just add it
                self.schemas[name] = copy.deepcopy(schema)
            else:
                # same schema, combine tables.
                # leaves all properties of source schema untouched.
                for table_name, table in schema.tables.items():
                    self.schemas[name].tables[table_name] = copy.deepcopy(table)
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

    def get_all_tables(self, only_names=False):
        """Helper function that returns all available tables (across schemas) in this metadata."""
        if self.schemas is None:
            return []
        tables = []
        for schema in self.schemas.values():
            if schema is not None:
                for table in schema.tables.values():
                    if only_names:
                        tables.append(table.name)
                    else:
                        tables.append(table)
        return tables

    def get_all_table_names(self):
        """Helper function that returns all available table names (across schemas) in this metadata."""
        return self.get_all_tables(only_names=True)

    def get_all_schema_names(self):
        """Helper function that returns a list of the names of all schemas in this metadata."""
        return [] if self.schemas is None else [schema_name for schema_name in self.schemas.keys()]

    def drop_columns_with_key_value(self, key, value):
        """Helper function that drops all columns from the metadata that have the given key value combination."""
        cols_to_drop = []
        for schema_key, schema in self.schemas.items():
            if schema is not None:
                for table_key, table in schema.tables.items():
                    for col_key, col in table.columns.items():
                        if getattr(col, key) == value:
                            cols_to_drop.append((schema_key, table_key, col_key))
        for col_to_drop in cols_to_drop:
            del self.schemas[col_to_drop[0]].tables[col_to_drop[1]].columns[col_to_drop[2]]

    def get_feature_target_cols(self):
        """gets all column name from all tables and looks if is_feature or is defined"""
        feature_cols = []
        target_cols = []

        tables = self.get_all_tables()
        for m_table in tables:
            for key in m_table.columns:
                col = m_table.columns[key]
                if col.is_feature:
                    feature_cols.append(key)
                if col.is_target:
                    target_cols.append(key)

        # conservative default. If not both list have elements fall back to the default values NONE
        if (len(feature_cols) == 0) or (len(target_cols) == 0):
            feature_cols = None
            target_cols = None
        return feature_cols, target_cols

    def get_col_types(self):
        """get all column names and type from all tables"""
        col_types = {}

        tables = self.get_all_tables()
        for m_table in tables:
            for key in m_table.columns:
                col = m_table.columns[key]
                col_types[key] = col.type
        return col_types

    def get_header(self):
        tables = self.get_all_tables()
        header = []
        for m_table in tables:
            header.append(m_table.header_row)
        return header


class Schema():
    """Schema class.

    Describes a data source unit via metadata information.

    Attributes:
        connection: data source connection URI
        name: name of the database
        size: the size of this database
        privacy_budget: parsed privacy budget property.
        privacy_budget_interval_days: parsed privacy budget reset interval in days.
        synth_allowed: true to allow synthesized data for exploration
        privacy_level: 0, 1, 2 in ascending order of privacy protection (default is 2).
        tables: parsed database metadata.
    """
    def __init__(
            self,
            name,
            size=0,
            connection='',
            privacy_budget=0,
            privacy_budget_interval_days=0,
            synth_allowed=False,
            privacy_level=2,
            tables=None):
        """Creates a new schema object."""
        self.name = name
        self.size = size
        self.connection = connection
        self.privacy_budget = privacy_budget
        self.privacy_budget_interval_days = privacy_budget_interval_days
        self.synth_allowed = synth_allowed
        self.privacy_level = privacy_level
        self.tables = tables

    @staticmethod
    def from_meta(schema, meta):
        """Create a schema instance from the meta yaml part."""
        connection = meta.pop("connection", '')
        size = int(meta.pop("size", 0))
        privacy_budget = float(meta.pop("privacy_budget", 0))
        privacy_budget_interval_days = int(meta.pop("privacy_budget_interval_days", 0))
        synth_allowed = bool(meta.pop("synth_allowed", False))
        privacy_level = int(meta.pop("privacy_level", 2))
        tables = {}
        for table in meta.keys():
            tables[table] = Table.from_meta(table, meta[table])
        return Schema(
            schema,
            size=size,
            connection=connection,
            privacy_budget=privacy_budget,
            privacy_budget_interval_days=privacy_budget_interval_days,
            synth_allowed=synth_allowed,
            privacy_level=privacy_level,
            tables=tables
        )

    def to_dict(self, sm=False):  # noqa: C901
        """Returns a dict representation of this class."""
        meta = {}
        if not sm:
            if self.connection is not None:
                meta["connection"] = self.connection
            if self.size is not None:
                meta["size"] = self.size
            if self.privacy_budget is not None:
                meta["privacy_budget"] = self.privacy_budget
            if self.privacy_budget_interval_days is not None:
                meta["privacy_budget_interval_days"] = self.privacy_budget_interval_days
            if self.synth_allowed is not None:
                meta["synth_allowed"] = self.synth_allowed
            if self.privacy_level is not None:
                meta["privacy_level"] = self.privacy_level
        for table in self.tables:
            meta[table] = self.tables[table].to_dict(sm=sm)
        return meta


class Table():
    """Table represents a table definition inside the metadata."""
    def __init__(
            self,
            name,
            use_original_header=True,
            header_row=None,
            header_columns=None,
            row_privacy=False,
            rows=0,
            max_ids=1,
            sample_max_ids=True,
            use_dpsu=False,
            clamp_counts=False,
            clamp_columns=True,
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
        self.use_original_header = use_original_header
        self.header_row = header_row
        self.header_columns = header_columns
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
        use_original_header = bool(meta.pop(
            "use_original_header", True))
        header_row = meta.pop("header_row", None)
        header_columns = meta.pop("header_columns", None)
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
            use_original_header=use_original_header,
            header_row=header_row,
            header_columns=header_columns,
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
            if self.use_original_header is not None:
                meta["use_original_header"] = self.use_original_header
        if self.header_row is not None:
            meta["header_row"] = self.header_row
        if self.header_columns is not None:
            meta["header_columns"] = self.header_columns
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
            mask=None,
            synthesizable=True,
            discrete=False,
            min_step=1.0,
            is_feature=False,
            is_target=False):
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
        self.synthesizable = synthesizable
        self.discrete = discrete
        self.min_step = min_step
        self.is_feature = is_feature
        self.is_target = is_target

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
        synthesizable = bool(meta["synthesizable"]) if "synthesizable" in meta else True
        discrete = False
        min_step = 1.0
        if _type == "boolean":
            if "synthesizable" not in meta:
                synthesizable = False
        elif _type == "datetime":
            if "synthesizable" not in meta:
                synthesizable = False
        elif _type == "int":
            lower = int(meta["lower"]) if "lower" in meta else None
            upper = int(meta["upper"]) if "upper" in meta else None
            auto_lower = int(meta["auto_lower"]) if "auto_lower" in meta else None
            auto_upper = int(meta["auto_upper"]) if "auto_upper" in meta else None
            discrete = bool(meta["discrete"]) if "discrete" in meta else False
            min_step = int(meta["min_step"]) if "min_step" in meta else None
        elif _type == "float":
            lower = float(meta["lower"]) if "lower" in meta else None
            upper = float(meta["upper"]) if "upper" in meta else None
            auto_lower = float(meta["auto_lower"]) if "auto_lower" in meta else None
            auto_upper = float(meta["auto_upper"]) if "auto_upper" in meta else None
            discrete = bool(meta["discrete"]) if "discrete" in meta else False
            min_step = float(meta["min_step"]) if "min_step" in meta else None
        elif _type == "string":
            cardinality = int(meta["cardinality"]) if "cardinality" in meta else 0
            allowed_values = meta["allowed_values"] if "allowed_values" in meta else None
            mask = meta["mask"] if "mask" in meta else None
            if "synthesizable" not in meta:
                synthesizable = False if cardinality == 0 else True
        else:
            raise ValueError("Unknown column type {} for column {}".format(_type, column))
        private_id = bool(meta["private_id"]) if "private_id" in meta else False
        selectable = bool(meta["selectable"]) if "selectable" in meta else False
        is_feature = bool(meta["is_feature"]) if "is_feature" in meta else False
        is_target = bool(meta["is_target"]) if "is_target" in meta else False
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
            mask=mask,
            synthesizable=synthesizable,
            discrete=discrete,
            min_step=min_step,
            is_feature=is_feature,
            is_target=is_target
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
        if self.cardinality is not None:
            meta["cardinality"] = self.cardinality
        if not sm:
            if self.use_auto_bounds is not None:
                meta["use_auto_bounds"] = self.use_auto_bounds
            if self.auto_bounds_prob is not None:
                meta["auto_bounds_prob"] = self.auto_bounds_prob
            if self.auto_lower is not None:
                meta["auto_lower"] = self.auto_lower
            if self.auto_upper is not None:
                meta["auto_upper"] = self.auto_upper
            if self.allowed_values is not None:
                meta["allowed_values"] = self.allowed_values
            if self.selectable is not None:
                meta["selectable"] = self.selectable
            if self.mask is not None:
                meta["mask"] = self.mask
            if self.synthesizable is not None:
                meta["synthesizable"] = self.synthesizable
            if self.discrete is not None:
                meta["discrete"] = self.discrete
            if self.min_step is not None:
                meta["min_step"] = self.min_step
            if self.is_feature is not None:
                meta["is_feature"] = self.is_feature
            if self.is_target is not None:
                meta["is_target"] = self.is_target
        return meta
