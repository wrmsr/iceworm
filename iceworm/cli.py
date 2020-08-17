import argparse
import glob
import logging
import re
import time
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import logs
from omnibus import properties

from .trees import analysis
from .trees import parsing
from .trees import rendering


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
        _arg('--not', dest='not_pats', action='append'),
        _arg('--strip-header', action='store_true'),
        _arg('--rounds', type=int),
    )
    def cmd_run(self) -> None:
        not_pats = [re.compile(n) for n in self.args.not_pats] if self.args.not_pats else []

        paths = set()
        for glob_pat in self.args.glob or []:
            for path in glob.iglob(glob_pat, recursive=True):
                skip = False
                for not_pat in not_pats:
                    if not_pat.match(path):
                        log.info(f'Skipping : {path}')
                        skip = True
                        break
                if skip:
                    continue
                paths.add(path)
        paths = sorted(paths)

        for i, path in enumerate(paths * (self.args.rounds or 1)):
            log.info(f'Parsing {i} / {len(paths)} ({i * 100. / len(paths):0.02f}%) : {path}')

            with open(path, 'r') as f:
                txt = f.read()
            txt = txt.lower()

            if self.args.strip_header:
                lines = txt.splitlines()
                for i in range(len(lines)):
                    if lines[i].strip() == '---':
                        lines = lines[i+1:]
                        break
                txt = '\n'.join(lines)

            try:
                start = time.time()
                root = parsing.parse_statement(txt)  # noqa
                end = time.time()

                basic = analysis.basic(root)
                log.info(f'Parsed {len(basic.nodes)} nodes after {(end - start) * 1000.:0.02f} ms')

                rendered = rendering.render(root)
                reparsed = parsing.parse_statement(rendered + ';')
                if reparsed != root:
                    raise ValueError('Reparse failed')

            except Exception as e:  # noqa
                log.exception('Parse failure')

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
