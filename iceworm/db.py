import configparser
import io
import os
import typing as ta

from omnibus import lang


@lang.cached_nullary
def get_config() -> ta.Mapping[str, str]:
    config_file_path = os.environ['SNOWFLAKE_CONFIG_PATH']
    with open(os.path.expanduser(config_file_path), 'r') as f:
        txt = f.read()

    parser = configparser.ConfigParser()
    parser.read_file(io.StringIO(txt))
    return {k.lower(): v for k, v in parser.items('snowflake')}


@lang.cached_nullary
def get_url() -> str:
    cfg = get_config()
    not_url_params = {'user', 'password', 'host'}
    url_params = {k.lo: v for k, v in cfg.items() if k not in not_url_params}
    return (
            'snowflake://' +
            cfg['user'] +
            ((':' + cfg['password']) if 'password' in cfg else '') +
            '@' +
            cfg['host'] +
            '/' +
            (('?' + '&'.join(f'{k}={v}' for k, v in url_params.items())) if url_params else '')
    )
