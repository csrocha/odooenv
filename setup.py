#!/usr/bin/env python
from setuptools import setup

setup(
    name='odooenv',
    version='2.2.14',
    author='Cristian S. Rocha',
    author_email='cristian.rocha@moldeo.coop',
    maintainer='Cristian S. Rocha',
    maintainer_email='csr@moldeo.coop',
    url='https://github.com/csrocha/odooenv',
    download_url='https://github.com/csrocha/odooenv/tarball/v2.2.3',
    description='Odoo Environment Manager',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Build Tools',
    ],
    scripts=['scripts/odooenv'],
    packages=['odooenv'],
    package_dir={'odooenv': 'odooenv'},
    package_data={'odooenv': ['data/*.yml']},
    test_suite='tests',
    install_requires=[
        'virtualenv', 'psycopg2', 'argparse', 'bzr', 'pyyaml',
        'oerplib', 'argcomplete', 'werkzeug'],
    dependency_links=[
        'http://pysvn.barrys-emacs.org/source_kits/pysvn-1.7.5.tar.gz'],
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
