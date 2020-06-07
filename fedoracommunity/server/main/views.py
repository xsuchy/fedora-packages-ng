# fedoracommunity/server/main/views.py


import flask
from flask import render_template, Blueprint

from ..updates import get_updates
from ..builds import get_builds
from ..packages import get_packages, get_package
from ..bugs import get_bugs
from ..changelogs import get_changelogs
from ...server import cache

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


@main_blueprint.route("/", methods=["POST"])
def home_post():
    url = "/packages/s/{0}".format(flask.request.form["package_name"])
    return flask.redirect(url)


@main_blueprint.route("/packages/s/")
@main_blueprint.route("/packages/s/<package_name>/")
def packages_search(package_name=None):
    packages = get_packages(package_name)
    total = packages.count()
    return render_template("search_results.html",
                           packages=packages.all(), total=total,
                           package_name=package_name)


@main_blueprint.route("/packages/")
@main_blueprint.route("/packages/<package_name>/")
def packages(package_name=None):
    if not package_name:
        return home()
    else:
        package = get_package(package_name)
        return render_template("main/package-overview.html",
                               package=package)


@cache.cached(timeout=120)
@main_blueprint.route("/packages/<package_name>/builds")
def package_builds(package_name):
    package = get_package(package_name)
    builds = get_builds(package_name)
    return render_template("main/package-builds.html",
                           package=package, builds=builds)


@cache.cached(timeout=120)
@main_blueprint.route("/packages/<package_name>/updates")
def package_updates(package_name):
    package = get_package(package_name)
    updates = get_updates(package_name)
    return render_template("main/package-updates.html",
                           package=package, updates=updates)


@cache.cached(timeout=600)
@main_blueprint.route("/packages/<package_name>/bugs")
def package_bugs(package_name):
    package = get_package(package_name)
    bugs = get_bugs(package_name)
    return render_template("main/package-bugs.html",
                           package=package, bugs=bugs['bugs'],
                           open_bugs=bugs['open_bugs'],
                           open_bugs_url=bugs['open_bugs_url'],
                           blocker_bugs=bugs['blocker_bugs'],
                           blocker_bugs_url=bugs['blocker_bugs_url'],
                           )


@main_blueprint.route("/packages/<package_name>/problems")
def package_problems(package_name):
    package = get_package(package_name)
    return render_template("main/package-problems.html",
                           package=package)


@main_blueprint.route("/packages/<package_name>/contents")
def package_contents(package_name):
    package = get_package(package_name)
    return render_template("main/package-contents.html",
                           package=package)


@cache.cached(timeout=600)
@main_blueprint.route("/packages/<package_name>/changelog")
def package_changelog(package_name):
    package = get_package(package_name)
    changelog = get_changelogs(package_name)
    return render_template("main/package-changelog.html",
                           package=package,
                           changelog=changelog)


@main_blueprint.route("/packages/<package_name>/sources")
def package_sources(package_name):
    package = get_package(package_name)
    return render_template("main/package-sources.html",
                           package=package)
