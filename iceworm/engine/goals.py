"""
TODO:
 - all, backfill, ddl, check, ...
 - views are elements, goals are like backfill and day and ddl
  - goals take elements and make ops, ops get rewritten and shit
  - ‘rules’?
  - ‘subsystems’? muh
  - CreateTableAs = rule, 'create table foo as select * from …' = .. rule 'call'? 'instantiation'?, wo.View = element


./pants --changed-since=HEAD lint
./pants --changed-since=origin/main lint
--changed-dependees=direct or --changed-dependees=transitive
./pants --tag=integration_test list ::
./pants --tag='-integration_test' list ::
./pants --tag='+type_checked,skip_lint' --tags='-integration_test' list ::
./pants --spec-file=targets.txt list
./pants dependees helloworld/util | xargs ./pants  list

$ dbt run --models my_dbt_project_name   # runs all models in your project
$ dbt run --models my_dbt_model          # runs a specific model
$ dbt run --models path.to.my.models     # runs all models in a specific directory
$ dbt run --models my_package.some_model # run a specific model in a specific package
$ dbt run --models tag:nightly           # run models with the "nightly" tag
$ dbt run --models path/to/models        # run models contained in path/to/models
$ dbt run --models path/to/my_model.sql  # run a specific model by its path

$ dbt run --models my_model+          # select my_model and all children
$ dbt run --models +my_model          # select my_model and all parents
$ dbt run --models +my_model+         # select my_model, and all of its parents and children

$ dbt run --models my_model+1          # select my_model and its first-degree children
$ dbt run --models 2+my_model          # select my_model, its first-degree parents, and its second-degree parents ("grandparents")
$ dbt run --models 3+my_model+4        # select my_model, its parents up to the 3rd degree, and its children down to the 4th degree

The @ operator is similar to +, but will also include the parents of the children of the selected model.

$ dbt run --models snowplow.*      # run all of the models in the snowplow package
$ dbt run --models finance.base.*  # run all of the models in models/finance/base

Run all the common ancestors of snowplow_sessions and fct_orders:
$ dbt run --models +snowplow_sessions,+fct_orders

Run all the common descendents of stg_invoices and stg_accounts:
$ dbt run --models stg_invoices+,stg_accounts+

Run models that are in the marts/finance subdirectory and tagged nightly:
$ dbt run --models marts.finance,tag:nightly

$ dbt run --models my_package.*+ --exclude my_package.a_big_model+
Exclude a specific resource by its name or lineage:

# test
$ dbt test --exclude not_null_orders_order_id
$ dbt test --exclude orders

# seed
$ dbt seed --exclude account_parent_mappings

# snapshot
$ dbt snapshot --exclude snap_order_statuses
$ dbt test --exclude orders+

$ dbt run --models tag:nightly    # run all models with the `nightly` tag
$ dbt run --models source:snowplow+    # run all models that select from Snowplow sources

# These two selectors are equivalent
dbt run --models path:models/staging/github
dbt run --models models/staging/github

# These two selectors are equivalent
dbt run --models path:models/staging/github/stg_issues.sql
dbt run --models models/staging/github/stg_issues.sql

# These three selectors are equivalent
dbt run --models package:snowplow
dbt run --models snowplow
dbt run --models snowplow.*

$ dbt run --models config.materialized:incremental    # run all models that are materialized incrementally
$ dbt run --models config.schema:audit                # run all models that are created in the `audit` schema
$ dbt run --models config.cluster_by:geo_country      # run all models clustered by `geo_country`

$ dbt test --models test_type:schema        # run all schema tests
$ dbt test --models test_type:data          # run all data tests

$ dbt test --models test_name:unique            # run all instances of the `unique` test
$ dbt test --models test_name:equality          # run all instances of the `dbt_utils.equality` test
$ dbt test --models test_name:range_min_max     # run all instances of a custom schema test defined in the local project, `range_min_max`

$ dbt test --models state:new            # run all tests on new models + and new tests on old models
$ dbt run --models state:modified        # run all models that have been modified
$ dbt ls --models state:modified     # list all modified nodes (not just models)

$ dbt run --models my_package.*+      # select all models in my_package and their children
$ dbt run --models +some_model+       # select some_model and all parents and children

$ dbt run --models tag:nightly+       # select "nightly" models and all children
$ dbt run --models +tag:nightly+      # select "nightly" models and all parents and children

$ dbt run --models @source:snowplow   # build all models that select from snowplow sources, plus their parents

$ dbt test --models config.incremental_strategy:insert_overwrite,test_name:unique   # execute all `unique` tests that select from models using the `insert_overwrite` incremental strategy

$ dbt run --models @source:snowplow,tag:nightly models/export --exclude package:snowplow,config.materialized:incremental export_performance_timing

selectors:
  - name: nightly_diet_snowplow
    definition:
      union:
        - intersection:
            - '@source:snowplow'
            - 'tag:nightly'
        - 'models/export'
        - exclude:
            - intersection:
                - 'package:snowplow'
                - 'config.materialized:incremental'
            - export_performance_timing
"""
import typing as ta

from omnibus import dataclasses as dc


class Goal(dc.Enum):

    @property
    def name(self) -> ta.Optional[str]:
        return None


class Invalidate(Goal):
    pass
