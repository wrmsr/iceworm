import fnmatch
import os
import sys
import warnings

import setuptools.command.build_ext

import distutils.cmd
import distutils.log


if sys.version_info < (3, 7):
    raise EnvironmentError('python >= 3.7 required')


warnings.filterwarnings(
    'ignore',
    message=r"Normalizing '[^'-]+-[^'-]+' to '[^'-]+\.[^'-]+'",
    module=r'setuptools\.dist',
)


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

    'Jinja2>=2.11',
    'protobuf>=3.13',
    'PyYAML>=5.3',
    'SQLAlchemy>=1.3',

    # @omnibus-dep@
    'omnibus @ git+https://github.com/wrmsr/omnibus@4ce8f94e5176577bed1f19421fc9b0447d045957',

]

EXTRAS_REQUIRE = {
}

EXT_MODULES = [
]


class CyamlCommand(distutils.cmd.Command):
    description = 'install cyaml'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce('Installing cyaml')

        import tempfile
        dp = tempfile.mkdtemp()

        import os.path
        fp = os.path.join(dp, 'cyaml.tar.gz')

        import urllib.request
        urllib.request.urlretrieve('http://pyyaml.org/download/pyyaml/PyYAML-5.3.1.tar.gz', fp)

        import sys
        os.system(
            f'cd {dp} && '
            f'{os.path.abspath(sys.executable)} -m pip install cyaml.tar.gz --global-option="--with-libyaml"'
        )


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        cmdclass={
            'cyaml': CyamlCommand,
        },

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

        entry_points={
            'console_scripts': [
                f'{PROJECT} = {PROJECT}.cli:main',
            ],
        },

        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,

        ext_modules=EXT_MODULES,
    )
