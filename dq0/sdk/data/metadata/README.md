# DQ0 Data Source Metadata

Metadata definitions are used to define properties of data sets. The metadata completely describes the dataset. However, it does not include any information about how to access the dataset (connection string etc).

The metadata properties include:

* name
* description
* type
* row level information, if applicable, with
  * row level privacy
* columns, if applicable, with
  * type
  * lower and upper bound (DP)
  * privacy constraints
  * masking: regex masks away groups, shows anything else
  * DP privacy ID info
* initial privacy budget
* privacy budget reset interval

Metadata is stored in DQ0's central database. It can be defined in the web application or via yaml files. The inner definition in "Database" shall be compatible with [smartnoise metadata](https://github.com/opendifferentialprivacy/smartnoise-sdk/blob/master/sdk/Metadata.md). A yaml metadata definition can look like this:

```yaml
name: 'sample data 1'
description: 'some description'
type: 'tabular'
privacy_budget: 1000
privacy_budget_interval_days: 30
database:
    Table1:
        row_privacy: true
        rows: 1000
        max_ids: 1
        sample_max_ids: true
        censor_dims: false
        user_id:
            private_id: true
            type: int
        weight:
            type: float
            lower: 0.0
            upper: 100.0
        name:
            type: string
            hide: true
        email:
            type: string
            mask: '(.*)@(.*).{3}$'
```