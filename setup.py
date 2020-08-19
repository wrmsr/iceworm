import fnmatch
import os
import sys

import setuptools.command.build_ext


PROJECT = 'iceworm'

BASE_DIR = os.path.dirname(__file__)
ABOUT = {}


def _read_about():
    with open(os.path.join(BASE_DIR, PROJECT, '__about__.py'), 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ABOUT)


_read_about()


EXCLUDED_STATIC_FILE_PATHS = [
    '*.py',
    '*/__pycache__/*',
    '*/tests/*',
]


def _get_static_files(path):
    return [
        filepath
        for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True)
        for filename in filenames
        for filepath in [os.path.join(dirpath, filename)]
        if not any(fnmatch.fnmatch(filepath, pat) for pat in EXCLUDED_STATIC_FILE_PATHS)
    ]


PACKAGE_DATA = [
] + _get_static_files(PROJECT)


INSTALL_REQUIRES = [
]

EXTRAS_REQUIRE = {
}

EXT_MODULES = [
]


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        python_requires=ABOUT['__python_requires__'],
        classifiers=ABOUT['__classifiers__'],

        setup_requires=['setuptools'],

        packages=setuptools.find_packages(
            include=[PROJECT, PROJECT + '.*'],
            exclude=['tests', '*.tests', '*.tests.*'],
        ),
        py_modules=[PROJECT],

        package_data={PROJECT: PACKAGE_DATA},
        include_package_data=True,

        entry_points={},

        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,

        ext_modules=EXT_MODULES,
    )
