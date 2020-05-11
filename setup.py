#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages
import io
from os.path import join
from os.path import dirname
from os.path import splitext
from os.path import basename
from glob import glob


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name="ldap3_demo",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.8',
)
