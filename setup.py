import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

requires = ['click']
tests_requires = ['pytest', 'pytest-cache', 'pytest-cov']
lint_requires = ['flake8', 'black']
dev_requires = requires + tests_requires + lint_requires


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="connectors-utility-cli",
    version='0.0.0',
    description="A combination different connectors acting as proxies to data sources",
    long_description="\n\n".join([open("README.md").read()]),
    license='MIT',
    author="Hong Nguyen",
    author_email="hpnguyen@linkedin.com",
    url="https://connectors-utility-cli.readthedocs.org",
    packages=find_packages(),
    install_requires=requires,
    entry_points={'console_scripts': [
        'connect = connectors_utility.cli:main',
        'msgraph = connectors_utility.msgraph.cli:main',
        'gsheet = connectors_utility.google.cli:main'
    ]},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython'],
    extras_require={
        'test': tests_requires,
        'dev': dev_requires,
        'lint': lint_requires,
    },
    cmdclass={'test': PyTest})
