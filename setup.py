# -*- coding: utf-8 -*-
# This file is part of Fedora Community.
# Copyright (C) 2008-2013  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob

# These two imports are not actually used, but are required to stop tests from
# failing on python 2.7.
import multiprocessing
import logging
import koji

from setuptools import setup, find_packages


def find_data():
    here = os.path.dirname(os.path.realpath(__file__))
    datadir = os.path.join(here, "fedoracommunity/client")
    data = []
    for root, dirs, files in os.walk(datadir):
        for f in files:
            path = os.path.join(root, f)
            path = path.replace(here + "/fedoracommunity/", "")
            data.append(path)
    return data


setup(
    name='fedoracommunity',
    version='5.5.0',
    description='',
    license='AGPLv3',
    authors=('John (J5) Palmieri <johnp@redhat.com>',
             'Luke Macken <lmacken@redhat.com>',
             'Máirín Duffy <duffy@redhat.com>',
             'Ralph Bean <rbean@redhat.com>',
             ),
    url='https://github.com/fedora-infra/fedora-packages',
    install_requires=[
        "bodhi-client",
        "python-bugzilla",
        "flask-bootstrap",
        "flask-cache",
        "flask-migrate",
        "flask-sqlalchemy",
        "paste",
        "pdc-client",
        "humanize",
        "koji",
        "requests",
        "markdown",
        "fedmsg",
        # python3-xapian does not provide python3.8dist(xapian)
        #"xapian",
        ],
    scripts=['bin/index-packages'],
    packages=find_packages(),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['webtest'],
    package_data={'fedoracommunity': find_data()},

    #entry_points="""
    #[setuptools.file_finders]
    #git = fedoracommunity.lib.utils:find_git_files

    #[paste.app_factory]
    #main = fedoracommunity.config.middleware:make_app

    #[paste.app_install]
    #main = pylons.util:PylonsInstaller

    #"""
)
