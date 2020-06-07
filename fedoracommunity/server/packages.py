from . import xapian_cache as db
from .models import Package
from .exceptions import ObjectNotFound


def get_packages(querystring):
    query = db.search(querystring)
    query.model = Package
    return query


def get_package(package_name):
    package = db.search_one(package_name)
    if not package:
        raise ObjectNotFound("Package {0} was not found".format(package_name))
    return Package(package)
