from setuptools import setup, find_packages

from proxy_overrides import VERSION

README = open('README.rst').read()

setup(
    name='django-proxy-overrides',
    version='.'.join(map(str, VERSION)),
    description='Overridable foreign key fields for Proxy models',
    long_description=README,
    url='https://github.com/datamade/django-proxy-overrides',
    author='Matthew Schinckel',
    author_email='matt@schinckel.net',
    maintainer='Forest Gregg',
    maintainer_email='fgregg@datamade.us',
    packages=find_packages(exclude=('tests*',)),
    install_requires=['Django'],
    test_suite='runtests.runtests',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
