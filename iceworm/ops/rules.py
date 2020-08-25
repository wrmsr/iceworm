"""
TODO:
 - test harness
 - debug as py
 - pure ops - pandas
 - omnibus.interp
 - opinionated src layout - git vs zipfile
 - static ana - not just no getattr but take both if branches
  - know expr origins of branches, can tell if const

yes:
 - loops
 - jinja (much stricter context but loops okay)
 - maybe sqla core
 - core api
 - maybe in-repo file io

no:
 - env vars - api.config('key'), returns *placeholder* like bindparam
 - db io
 - service io
 - current date/time (use sa.func.now(), rewritten in transforms)
 - 'run' date/time - no concept of that

- 'query': string literal, file: sql/py
 - when py, a module containing a function named 'query', *injected*
 - def query(now: iwa.now) -> str: …
 - setup.py entrypoint format - default 'query' or 'foo.py:q1'
"""
class Macro:
    pass


class Rule:
    pass


class Target:
    pass
