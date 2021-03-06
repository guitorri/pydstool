#!/usr/bin/env python
"""
Setup script for PyDSTool

This uses Distutils, the standard Python mechanism for installing packages.
For the easiest installation just type::

    python setup.py install

(root privileges probably required). If you'd like to install only for local user,
type the following to install PyDSTool::

    python setup.py install --user

In addition, there are some other commands::

python setup.py clean - Clean all trash (*.pyc, emacs backups, etc.)
python setup.py test  - Run test suite

"""


from setuptools import setup, os, find_packages
from setuptools.command.test import test as TestCommand
from setuptools import Command
import sys

vernum_major = '0.88'
vernum_minor = '140328'
vernum = vernum_major+'.'+vernum_minor
__version__  = vernum
__revision__ = '$Revision: %s $' % vernum_minor
__date__     = '$Date: 2014/03/28 00:00:00 $'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def check_dependency_versions():
    if sys.version_info[:2] < (2, 6) or (3, 0) <= sys.version_info[0:2] < (3, 3):
        raise RuntimeError("Python version 2.6, 2.7 or >= 3.3 required.")


class clean(Command):
    description = 'Remove build and trash files'
    user_options = [("all", "a", "the same")]

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        import os
        os.system(
            "rm -fr ./*.pyc ./*~ ./*/*.pyc ./*/*~ ./*/*/*.pyc ./*/*/*~ ./*/*/*.so ./PyDSTool/tests/auto_temp ./PyDSTool/tests/dopri853_temp ./PyDSTool/tests/radau5_temp ./PyDSTool/tests/dop853* ./PyDSTool/tests/radau5* ./PyDSTool/tests/*.pkl ./PyDSTool/tests/fort.9")
        os.system("rm -rf tests/radau5_temp tests/dopri853_temp radau5_temp dopri853_temp")
        os.system("rm -fr build")
        os.system("rm -fr dist")
        # os.system("rm -fr doc/_build")


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [a for a in self.test_args if a is not None]
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        import os
        os.system("rm -rf dopri853_temp radau5_temp auto_temp")
        sys.exit(errno)


check_dependency_versions()
setup(
    name="PyDSTool",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "six",
        "scipy>=0.9",
        "numpy>=1.6"
    ],
    tests_require=['pytest', 'mock', 'pytest-xdist'],
    cmdclass={
        'test': PyTest,
        'clean': clean
    },
    author="Rob Clewley; W. Erik Sherwood; M. Drew Lamar; Vladimir Zakharov",
    author_email="rob.clewley@gmail.com",
    maintainer="Rob Clewley",
    maintainer_email="rob.clewley@gmail.com",
    description=("Python dynamical systems simulation and modeling"),
    long_description = read('README.rst'),
    license = "BSD",
    keywords = "dynamical systems, bioinformatics, modeling, bifurcation analysis",
    url = "http://pydstool.sourceforge.net",
    include_package_data=True,
    platforms = ["any"],
    package_data = {
        '': ['*.txt', '*.rst'],
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: Linux",
    ],
)
