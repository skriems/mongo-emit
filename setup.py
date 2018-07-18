#!/usr/bin/env python

# Project skeleton maintained at gitlab://support/skeleton
# based on https://github.com/jaraco/skeleton

import setuptools

name = 'mongo-emit'
dashname = name.replace('_', '-')
description = 'MongoDB ChangeStream Emitter'
nspkg_technique = 'managed'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
    name=name,
    use_scm_version=True,
    author="Sebastian Kriems",
    author_email="gmail.at.bastobuntu",
    description=description or name,
    url='https://github.com/skriems/mongo-emit',
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=(
        name.split('.')[:-1] if nspkg_technique == 'managed'
        else []
    ),
    python_requires='>=3.6',
    install_requires=[
        'pymongo>=3.7.1',
        'python-dateutil>=2.7.3',
        'pytz>=2018.5',
        'yamlreader>=3.0.4'
    ],
    extras_require={
        'testing': [
            # upstream
            'pytest>=3.5',
            'pytest-sugar>=0.9.1',
            'collective.checkdocs',
            'pytest-flake8',

            # local
        ],
        'docs': [
            # upstream
            'sphinx',
            'jaraco.packaging>=3.2',
            'rst.linker>=1.9',

            # local
        ],
    },
    setup_requires=[
        'setuptools_scm>=1.15.0',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'mongo-emit = mongo_emit:run'
        ]
    }
)
if __name__ == '__main__':
    setuptools.setup(**params)
