from . import xapian_cache as db
from .models import Package


def get_packages(querystring):
    query = db.search(querystring)
    query.model = Package
    return query


def get_package(package_name):
    query = db.search_one(package_name)
    query.model = Package
    return query.all()[0]
