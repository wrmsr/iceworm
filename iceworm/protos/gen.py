"""
TODO:
 - enums
 - record revision
 - nodal/serde polymorphism -> https://stackoverflow.com/a/35748115 :/
 - ** auto-name with CamelCased package name **
  - unless overridden w a anno
"""
import logging
import os.path
import subprocess
import sys
import typing as ta

from omnibus import argparse as oap
from omnibus import check
from omnibus import code as ocod
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import logs
from omnibus import properties

from .. import __about__
from .registry import _PROTO_OBJS


log = logging.getLogger(__name__)


PACKAGE = __package__.split('.')[0]
JAVA_PREFIX = 'com.' + __about__.__author__


def _ver_tup(s: str) -> ta.Sequence[int]:
    return tuple(map(int, s.strip().split('.')))


class Gen:

    def __init__(
            self,
            *,
            package: str = PACKAGE,
            objs: ta.Optional[ta.Iterable[ta.Any]] = None,
            output_file_path: ta.Optional[str] = None,
            compile: bool = False,
            import_roots: ta.Iterable[str] = (),
            java_prefix: ta.Optional[str] = JAVA_PREFIX,
    ) -> None:
        super().__init__()

        self._package = package
        self._objs = list(objs) if objs is not None else None
        self._output_file_path = output_file_path
        self._compile = compile
        self._import_roots = list(check.isinstance(e, str) for e in (check.not_isinstance(import_roots, str) or []))
        self._java_prefix = java_prefix

        self._out = ocod.IndentWriter(indent='  ')

    @lang.cached_nullary
    def get_protoc_ver_str(self) -> str:
        return subprocess.check_output(['protoc', '--version']).decode('utf-8').strip()

    @lang.cached_nullary
    def get_protoc_ver_tup(self) -> ta.Sequence[int]:
        buf = self.get_protoc_ver_str()
        check.state(buf.startswith('libprotoc '))
        return _ver_tup(buf.partition(' ')[2])

    @properties.cached
    def lib_ver_tup(self) -> ta.Sequence[int]:
        import google.protobuf
        return _ver_tup(google.protobuf.__version__)

    @lang.cached_nullary
    def gen(self) -> str:
        if self._compile:
            lib_ver_tup = self.lib_ver_tup
            bin_ver_tup = self.get_protoc_ver_tup()
            if lib_ver_tup[:2] != bin_ver_tup[:2]:
                raise EnvironmentError(
                    f'protobuf versions out of sync: lib={lib_ver_tup}, bin={bin_ver_tup}. '
                    f'please update {"lib" if bin_ver_tup > lib_ver_tup else "bin"}.'
                )

        for ir in self._import_roots:
            log.info(f'Importing {ir}')
            for ie in lang.yield_import_all(ir, recursive=True):
                log.info(f'Imported {ie}')

        if self._objs is None:
            self._objs = [o for n, o in sorted(_PROTO_OBJS.items(), key=lambda t: t[0])]

        self._out.write('syntax = "proto3";\n')
        self._out.write('\n')
        self._out.write(f'package {self._package};\n')
        self._out.write('\n')

        if self._java_prefix:
            self._out.write(f'option java_package = "{self._java_prefix}.{self._package}";\n')
            self._out.write('\n')

        self._out.write('\n')

        for obj in self._objs:
            self._gen_obj(obj)
            self._out.write('\n')
            self._out.write('\n')

        src = self._out.getvalue().strip() + '\n'

        if self._output_file_path is not None:
            with open(self._output_file_path, 'w') as f:
                f.write(src)

            if self._compile:
                subprocess.check_call(
                    [
                        'protoc',
                        '-I=.',
                        '--python_out=.',
                        os.path.basename(self._output_file_path),
                    ],
                    cwd=os.path.dirname(self._output_file_path),
                    stderr=sys.stderr,
                )

                cfp = self._output_file_path.rpartition('.')[0] + '_pb2.py'
                with open(cfp, 'r') as f:
                    csrc = f.read()
                with open(cfp, 'w') as f:
                    f.write('# flake8: noqa\n')
                    f.write(f'# protoc: {self.get_protoc_ver_str()}\n')
                    f.write(csrc)

        return src

    def _gen_obj(self, obj: ta.Any) -> None:
        if isinstance(obj, type) and dc.is_dataclass(obj):
            self._gen_dc(obj)
        else:
            raise TypeError(obj)

    def _gen_dc(self, cls: type) -> None:
        log.info(f'Generating dataclass {cls}')

        self._out.write(f'// {cls.__module__}.{cls.__qualname__}\n')

        self._out.write(f'message {cls.__name__} {{\n')

        with self._out.indent():
            for i, fld in enumerate(dc.fields(cls)):
                if fld.type == str:
                    ty = 'string'
                elif fld.type == int:
                    ty = 'int32'
                elif fld.type == float:
                    ty = 'float'
                else:
                    raise TypeError(fld.type)

                self._out.write(f"{ty} {fld.name} = {i + 1};\n")

        self._out.write('}\n')


class Cli(oap.Cli):

    @oap.command()
    def gen(self) -> None:
        gen = Gen(
            output_file_path=os.path.join(os.path.dirname(__file__), '_gen', PACKAGE + '.proto'),
            compile=True,
            import_roots=[PACKAGE],
        )
        gen.gen()


def main():
    logs.configure_standard_logging(logging.INFO)
    Cli()()


if __name__ == '__main__':
    main()
