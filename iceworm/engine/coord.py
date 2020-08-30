"""
TODO:
 - masterless, so through pg coord
  - do we have skip locked
   - yea https://www.2ndquadrant.com/en/blog/what-is-select-skip-locked-for-in-postgresql-9-5/
 - scheduling pushed into db
  - ** interfaced ** - STILL HAVE IN-MEM DBG SCHED (+ STORE)
 - lol, push inval ranges into db?
  - ** ROWS TARGETS CANNOT OVERLAP **
  - would basically turn class Domain into tables - recursive cte for intersection
 - inval scheds - why? do-it-then-anyway? awaiting-multiple?
  - coalesce - do not rebuild every time, wait until optimal
 - self-query killer
"""
