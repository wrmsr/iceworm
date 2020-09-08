"""
TODO:
 - expanded reflection - partitioning etc
 - https://docs.snowflake.com/en/sql-reference/functions/compress.html udf payloads? lol

show locks:
 resource
 type
 transaction
 transaction_started_on
 status
 acquired_on
 query_id

show transactions
 id
 user
 session
 name
 started_on
 state

show external functions
 created_on
 name
 schema_name
 is_builtin
 is_aggregate
 is_ansi
 min_num_arguments
 max_num_arguments
 arguments
 description
 catalog_name
 is_table_function
 valid_for_clustering
 is_secure
 is_external_function

show streams
 name
 database_name
 schema_name
 owner
 comment
 table_name
 type
 stale
 mode
"""
import configparser
import io
import os
import typing as ta

from omnibus import check
from omnibus import lang
import sqlalchemy as sa
import sqlalchemy.ext.compiler  # noqa
import sqlalchemy.sql.selectable  # noqa

from .adapter import Adapter


EXEC_MULTI_SP_SRC = """
create or replace procedure exec_multi(stmts variant)
    returns variant language javascript as $$
    var sfstmts = [];
    for (var i = 0; i < STMTS.length; ++i) {
        var arg = STMTS[i];
        var sfstmt;
        if (Array.isArray(arg)) {
            sfstmt = snowflake.createStatement({
                sqlText: arg[0],
                binds: arg.slice(1),
            });
        }
        else if (typeof arg === "string") {
            sfstmt = snowflake.createStatement({
                sqlText: arg,
            });
        }
        else {
            throw "invalid arg";
        }
        sfstmts.push(sfstmt)
    }
    var ret = [];
    for (var i = 0; i < sfstmts.length; ++i) {
        var sfstmt = sfstmts[i];
        var rs = sfstmt.execute();
        var names = [];
        var types = [];
        for (var j = 1; ; ++j) {
            var cn;
            try {
                cn = rs.getColumnName(j);
            }
            catch (err) {
                break;
            }
            names.push(cn);
            types.push(rs.getColumnSqlType(j));
        }
        var rows = [];
        while (rs.next()) {
            var row = [];
            for (var j = 1; ; ++j) {
                var val;
                try {
                    val = rs.getColumnValue(j);
                }
                catch (err) {
                    break;
                }
                row.push(val);
            }
            rows.push(row);
        }
        ret.push({
            names: names,
            types: types,
            rows: rows,
        });
    }
    return ret;
$$ ;
"""


@lang.cached_nullary
def get_config() -> ta.Mapping[str, str]:
    config_file_path = os.environ['ICEWORM_SNOWFLAKE_CONFIG_PATH']
    with open(os.path.expanduser(config_file_path), 'r') as f:
        txt = f.read()

    parser = configparser.ConfigParser()
    parser.read_file(io.StringIO(txt))
    return {k.lower(): v for k, v in parser.items('snowflake')}


@lang.cached_nullary
def get_url() -> str:
    cfg = get_config()
    not_url_params = {'user', 'password', 'host'}
    url_params = {k.lower(): v for k, v in cfg.items() if k not in not_url_params}
    return (
            'snowflake://' +
            cfg['user'] +
            ((':' + cfg['password']) if 'password' in cfg else '') +
            '@' +
            cfg['host'] +
            '/' +
            (('?' + '&'.join(f'{k}={v}' for k, v in url_params.items())) if url_params else '')
    )


class Kwarg(sa.sql.expression.ClauseElement):

    def __init__(self, name, value):
        super().__init__()
        self.name = check.not_empty(check.isinstance(name, str))
        self.value = value


@sa.ext.compiler.compiles(Kwarg)
def visit_kwarg(element: Kwarg, compiler, **kwargs):
    return '%s => %s' % (
        element.name,
        compiler.process(element.value, **kwargs),
    )


kwarg = Kwarg


class SnowflakeAdapter(Adapter):

    @lang.override
    def build_range(self, num):
        # select seq4() i from table(generator(rowcount => 10))
        return sa.select([
            sa.func.seq4().label('i'),
        ]).select_from(
            sa.func.table(sa.func.generator(kwarg('rowcount', sa.literal(num))))
        )
