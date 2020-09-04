"""
TODO:
 - expanded reflection - partitioning etc

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

from omnibus import lang


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
