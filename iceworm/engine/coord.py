"""
TODO:
 - masterless, so through pg coord
  - do we have skip locked
   - yea https://www.2ndquadrant.com/en/blog/what-is-select-skip-locked-for-in-postgresql-9-5/
 - scheduling pushed into db
  - ** interfaced ** - STILL HAVE IN-MEM DBG SCHED (+ STORE)
 - lol, push inval ranges into db?
  - ** ROWS ELEMENTS CANNOT OVERLAP **
  - would basically turn class Domain into tables - recursive cte for intersection
 - inval scheds - why? do-it-then-anyway? awaiting-multiple?
  - coalesce - do not rebuild every time, wait until optimal
 - self-query killer
 - ** watchdog **
  - how to get progress? can snowflake give that? ui has something
   - * YES *
  - also: show locks
 - snowflake transactionality - and management re conns/sessions
  - grabbing locks at start of multiop, ensuring source tables dont mutate during - snowflake repeatable read..
 - ugh, need to impl a gil lol - continuous shared locks starve writers


Heartbeat:
select * from table(information_schema.query_history_by_session(24657760918758)) where execution_status = 'RUNNING'
https://docs.snowflake.com/en/sql-reference/functions/query_history.html

QUERY_ID TEXT
  The statement’s unique id.
QUERY_TEXT TEXT
  Text of the SQL statement.
DATABASE_NAME TEXT
  Database that was in use at the time of the query.
SCHEMA_NAME TEXT
  Schema that was in use at the time of the query.
QUERY_TYPE TEXT
  DML, query, etc. If the query is currently running, or the query failed, then the query type may be UNKNOWN.
SESSION_ID NUMBER
  Session that executed the statement.
USER_NAME TEXT
  User who issued the query.
ROLE_NAME TEXT
  Role that was active in the session at the time of the query.
WAREHOUSE_NAME TEXT
  Warehouse that the query executed on, if any.
WAREHOUSE_SIZE TEXT
  Size of the warehouse when this statement executed.
WAREHOUSE_TYPE TEXT
  Type of the warehouse when this statement executed.
CLUSTER_NUMBER NUMBER
  The cluster (in a multi-cluster warehouse) that this statement executed on.
QUERY_TAG TEXT
  Query tag set for this statement through the QUERY_TAG session parameter.
EXECUTION_STATUS TEXT
  Execution status for the query: resuming_warehouse, running, queued, blocked, success, failed_with_error, or
  failed_with_incident.
ERROR_CODE NUMBER
  Error code, if the query returned an error
ERROR_MESSAGE TEXT
  Error message, if the query returned an error
START_TIME TIMESTAMP_LTZ
  Statement start time
END_TIME TIMESTAMP_LTZ
  Statement end time. If the query is still running, the END_TIME is the UNIX epoch timestamp (“1970-01-01 00:00:00”),
  adjusted for the local time zone. E.g. for Pacific Standard Time, this would be “1969-12-31 16:00:00.000 -0800”.
TOTAL_ELAPSED_TIME NUMBER
  Elapsed time (in milliseconds)
BYTES_SCANNED NUMBER
  Number of bytes scanned by this statement.
ROWS_PRODUCED NUMBER
  Number of rows produced by this statement.
COMPILATION_TIME NUMBER
  Compilation time (in milliseconds)
EXECUTION_TIME NUMBER
  Execution time (in milliseconds)
QUEUED_PROVISIONING_TIME NUMBER
  Time (in milliseconds) spent in the warehouse queue, waiting for the warehouse servers to provision, due to warehouse
  creation, resume, or resize.
QUEUED_REPAIR_TIME NUMBER
  Time (in milliseconds) spent in the warehouse queue, waiting for servers in the warehouse to be repaired.
QUEUED_OVERLOAD_TIME NUMBER
  Time (in milliseconds) spent in the warehouse queue, due to the warehouse being overloaded by the current query
  workload.
TRANSACTION_BLOCKED_TIME NUMBER
  Time (in milliseconds) spent blocked by a concurrent DML.
OUTBOUND_DATA_TRANSFER_CLOUD TEXT
  Target cloud provider for statements that unload data to another region and/or cloud.
OUTBOUND_DATA_TRANSFER_REGION TEXT
  Target region for statements that unload data to another region and/or cloud.
OUTBOUND_DATA_TRANSFER_BYTES NUMBER
  Number of bytes transferred in statements that unload data to another region and/or cloud.
INBOUND_DATA_TRANSFER_CLOUD TEXT
  Source cloud provider for statements that load data from another region and/or cloud.
INBOUND_DATA_TRANSFER_REGION TEXT
  Source region for statements that load data from another region and/or cloud.
INBOUND_DATA_TRANSFER_BYTES NUMBER
  Number of bytes transferred in statements that load data from another region and/or cloud.
LIST_EXTERNAL_FILES_TIME NUMBER
  Time (in milliseconds) spent listing external files.
CREDITS_USED_CLOUD_SERVICES NUMBER
  Number of credits used for cloud services in the hour.
RELEASE_VERSION NUMBER
  Release version in the format of major_release.minor_release.patch_release.
EXTERNAL_FUNCTION_TOTAL_INVOCATIONS NUMBER
  The aggregate number of times that this query called remote services. For important details, see the Usage Notes.
EXTERNAL_FUNCTION_TOTAL_SENT_ROWS NUMBER
  The total number of rows that this query sent in all calls to all remote services.
EXTERNAL_FUNCTION_TOTAL_RECEIVED_ROWS NUMBER
  The total number of rows that this query received from all calls to all remote services.
EXTERNAL_FUNCTION_TOTAL_SENT_BYTES NUMBER
  The total number of bytes that this query sent in all calls to all remote services.
EXTERNAL_FUNCTION_TOTAL_RECEIVED_BYTES NUMBER
  The total number of bytes that this query received from all calls to all remote services.
"""
