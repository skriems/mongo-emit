#!/usr/bin/env python3
# -*- coding: utf-8 -*-

extensions = [
    'sphinx.ext.autodoc',
    'jaraco.packaging.sphinx',
    'rst.linker',
]

master_doc = 'index'

link_files = {
    '../CHANGES.rst': dict(
        using=dict(
            GH='https://github.com',
            devpi='https://devpi.yougov.net/root/yg',
            kiln='https://yougov.kilnhg.com/Code/Repositories',
            manuscript='https://yougov.manuscript.com',
            gitlab='https://gitlab.yougov.net',
        ),
        replace=[
            dict(
                pattern=r'(Case |\B#)(?P<issue>\d+)',
                url='{manuscript}/f/cases/{issue}/',
            ),
            dict(
                pattern=r'^(?m)((?P<scm_version>v?\d+(\.\d+){1,2}))\n[-=]+\n',
                with_scm='{text}\n{rev[timestamp]:%d %b %Y}\n',
            ),
            dict(
                pattern=r'PEP[- ](?P<pep_number>\d+)',
                url='https://www.python.org/dev/peps/pep-{pep_number:0>4}/',
            ),
            dict(
                pattern=r"queso (?P<queso_ver>\d+(\.\d+)*([abc]\d+)?)",
                url='{devpi}/queso/latest/+doc/history.html',
            ),
            dict(
                pattern=r"pan (?P<pan_ver>\d+(\.\d+)*([abc]\d+)?)",
                url='{devpi}/pan/latest/+doc/history.html',
            ),
        ],
    ),
}
