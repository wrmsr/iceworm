"""
TODO:
 - *not* named macro cuz jinja
 - macros return lists of / yield strs, statements
  - maybe other things but prob not
 - test harness
 - debug as py
 - pure ops - pandas
 - omnibus.interp
 - opinionated src layout - git vs zipfile
 - static ana - not just no getattr but take both if branches
 - know expr origins of branches, can tell if const
 - middle ground between whitebox and interpreted: importlib hook, enforce only touching api
  - iceworm.api vs iceworm_api.. latter safer, former more 'convenient' for deployment
  - same shit as omni.dev, sorta? would publish iw.zip + iw-api.zip
 - macros not discarded, macros not 'function calls'
  - macros are just ops, with an associated user-defined function that consumes it and emits more ops
  - maybe can get injected
  - 'call's? are removed from plan but retained for diagnosis, and are first class citizens - can be operated on
   - cifer 'metrics' are not discarded into a nest of tasks

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

https://www.microsoft.com/en-us/research/uploads/prod/2020/04/build-systems-jfp.pdf
https://www.lihaoyi.com/post/BuildToolsasPureFunctionalPrograms.html
https://www.lihaoyi.com/mill/page/mill-internals.html
https://github.com/pantsbuild/pants/blob/4f5462551a5023aced9277b4f4c7545f76bcd64d/src/python/pants/engine/query.py
https://github.com/pantsbuild/example-python
https://github.com/pantsbuild/example-plugin
https://www.pantsbuild.org/docs/target-api-concepts

https://medium.com/hashmapinc/dont-do-analytics-engineering-in-snowflake-until-you-read-this-hint-dbt-bdd527fa1795
https://github.com/fishtown-analytics/dbt
https://docs.getdbt.com/docs/building-a-dbt-project/building-models/materializations/
"""
import typing as ta

from omnibus import dataclasses as dc

from .. import metadata as md_
from ..types import QualifiedName
from .targets import Rule


class TableAsSelect(Rule):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table), kwonly=True)
