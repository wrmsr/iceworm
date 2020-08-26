import concurrent.futures as cf
import glob
import logging
import re
import time

from omnibus import argparse as oap
from omnibus import asyncs as oas
from omnibus import logs

from .trees import analysis
from .trees import parsing
from .trees import rendering
from .utils import multiprocessing as imp


log = logging.getLogger(__name__)


class Cli(oap.Cli):

    @oap.command(
        oap.arg('--glob', action='append'),
        oap.arg('--not', dest='not_pats', action='append'),
        oap.arg('--strip-header', action='store_true'),
        oap.arg('--rounds', type=int),
        oap.arg('-p', '--parallelism', type=int),
    )
    def run(self) -> None:
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

        def process(i: int, path: str) -> None:
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

        if self.args.parallelism:
            exe = cf.ProcessPoolExecutor(self.args.parallelism)
        else:
            exe = oas.ImmediateExecutor()

        oas.await_futures([
            exe.submit(process, i, path)
            for i, path in enumerate(paths * (self.args.rounds or 1))
        ])


def main():
    logs.configure_standard_logging(logging.INFO)

    def fn(i):
        print(i)
        pass

    with imp.forking_process_pool(fn, 1) as exe:
        oas.await_futures([exe.submit(fn, i) for i in range(10)])
        # oas.await_dependent_futures(exe, {functools.partial(f, i): {} for i in range(10)})

    exit(0)

    Cli()()


if __name__ == '__main__':
    main()
