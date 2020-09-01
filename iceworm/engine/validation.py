"""
TODO:
 - typecheck everything through day, and/or reactively
 - subsystem / thread / task / whatever to export all relevant connector schema regularly
  - put on s3, 'sites' configured to look there and dl / cahche / typecheck against locally + circle
 - check inferred types (vs both pg in dev and snow in circle+prod)
  - local tests, pre-commit
 - check all possible hits on all connectors for permissions
 - exploding ops into microops like s3 hits allows ahead-of-time traversal and checks like these that imperative doesn't
  - emails exist, owners exist
   - everyone the thing can email, just encode own internal emails in same iface as external
 - prod data bounds / stats
  - catch nullability, string convertibility, numeric bounds
 - * anomaly detection *
 - checks are rules
  - can annotate at cols and in header
  - expand to selects into their tables
  - further 'aspect' rules (just 'aspects'?) insert those into output tables like pd or slack or system.notifications

https://github.com/fishtown-analytics/dbt-utils

ge:
column_bootstrapped_ks_test_p_value_to_be_greater_than
column_chisquare_test_p_value_to_be_greater_than
column_distinct_values_to_be_in_set
column_distinct_values_to_contain_set
column_distinct_values_to_equal_set
column_kl_divergence_to_be_less_than
column_max_to_be_between
column_mean_to_be_between
column_median_to_be_between
column_min_to_be_between
column_most_common_value_to_be_in_set
column_pair_values_A_to_be_greater_than_B
column_pair_values_to_be_equal
column_pair_values_to_be_in_set
column_parameterized_distribution_ks_test_p_value_to_be_greater_than
column_proportion_of_unique_values_to_be_between
column_quantile_values_to_be_between
column_stdev_to_be_between
column_sum_to_be_between
column_to_exist
column_unique_value_count_to_be_between
column_value_lengths_to_be_between
column_value_lengths_to_equal
column_values_to_be_between
column_values_to_be_dateutil_parseable
column_values_to_be_decreasing
column_values_to_be_in_set
column_values_to_be_in_type_list
column_values_to_be_increasing
column_values_to_be_json_parseable
column_values_to_be_null
column_values_to_be_of_type
column_values_to_be_unique
column_values_to_match_json_schema
column_values_to_match_regex
column_values_to_match_regex_list
column_values_to_match_strftime_format
column_values_to_not_be_in_set
column_values_to_not_be_null
column_values_to_not_match_regex
column_values_to_not_match_regex_list
multicolumn_values_to_be_unique
table_column_count_to_be_between
table_column_count_to_equal
table_columns_to_match_ordered_list
table_row_count_to_be_between
table_row_count_to_equal
"""
