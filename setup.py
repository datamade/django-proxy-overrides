from setuptools import setup, find_packages

from proxy_overrides import VERSION

README = open('README.rst').read()

setup(
    name='django-proxy-overrides',
    version='.'.join(map(str, VERSION)),
    description='Overridable fields for Proxy models',
    long_description=README,
    author='Matthew Schinckel',
    author_email='matt@schinckel.net',
    packages=find_packages(exclude=('tests*',)),
    install_requires=['Django'],
    test_suite='runtests.runtests',
)
