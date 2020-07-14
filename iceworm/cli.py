import argparse
import glob
import logging
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import logs
from omnibus import properties

from . import parsing


log = logging.getLogger(__name__)


@dc.dataclass(frozen=True)
class _Arg:
    args: ta.Sequence[ta.Any] = ()
    kwargs: ta.Mapping[str, ta.Any] = ocol.frozendict()


def _arg(*args, **kwargs) -> _Arg:
    return _Arg(args, kwargs)


def _cmd(cmds, *args):
    def inner(fn):
        name = fn.__name__
        if not name.startswith('cmd_'):
            raise NameError(name)
        parser = cmds.add_parser(name[4:].replace('_', '-'))
        parser.set_defaults(fn=fn)
        for arg in args:
            parser.add_argument(*arg.args, **arg.kwargs)
        return fn

    return inner


class Cli:

    def __init__(self, raw_args=None) -> None:
        super().__init__()

        self._raw_args = raw_args

    parser = argparse.ArgumentParser()

    @properties.cached
    def args(self):
        return self.parser.parse_args(self._raw_args)

    cmds = parser.add_subparsers()

    @_cmd(
        cmds,
        _arg('--glob', action='append'),
        _arg('--strip-header', action='store_true'),
    )
    def cmd_run(self) -> None:
        for pat in self.args.glob:
            for path in glob.iglob(pat, recursive=True):
                log.info(f'Parsing {path}')

                with open(path, 'r') as f:
                    txt = f.read()

                if self.args.strip_header:
                    lines = txt.splitlines()
                    for i in range(len(lines)):
                        if lines[i].strip() == '---':
                            lines = lines[i+1:]
                            break
                    txt = '\n'.join(lines)

                try:
                    root = parsing.parse_statement(txt)  # noqa
                except Exception as e:  # noqa
                    log.exception('Parse failure')
                    log.error('Body:\n' + txt)

    def run(self) -> None:
        fn = getattr(self.args, 'fn', None)
        if fn is None:
            self.parser.print_help()
            return

        fn(self)


def main():
    logs.configure_standard_logging(logging.INFO)
    Cli().run()


if __name__ == '__main__':
    main()
