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

https://github.com/fishtown-analytics/dbt-utils
"""
