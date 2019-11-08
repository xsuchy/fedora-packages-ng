# project/server/main/views.py


from flask import render_template, Blueprint

from ..updates import get_updates
from ..builds import get_builds
from ..bugs import get_bugs
from ..changelogs import get_changelogs
from ...server import cache

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


@main_blueprint.route("/packages/")
@main_blueprint.route("/packages/<package_name>/")
def packages(package_name=None):
    if not package_name:
        return home()
    else:
        return render_template("main/package-overview.html",
                               package_name=package_name)


@cache.cached(timeout=120)
@main_blueprint.route("/packages/<package_name>/builds")
def package_builds(package_name):
    builds = get_builds(package_name)
    return render_template("main/package-builds.html",
                           package_name=package_name, builds=builds)


@cache.cached(timeout=120)
@main_blueprint.route("/packages/<package_name>/updates")
def package_updates(package_name):
    updates = get_updates(package_name)
    return render_template("main/package-updates.html",
                           package_name=package_name, updates=updates)


@cache.cached(timeout=600)
@main_blueprint.route("/packages/<package_name>/bugs")
def package_bugs(package_name):
    bugs = get_bugs(package_name)
    return render_template("main/package-bugs.html",
                           package_name=package_name, bugs=bugs['bugs'],
                           open_bugs=bugs['open_bugs'],
                           open_bugs_url=bugs['open_bugs_url'],
                           blocker_bugs=bugs['blocker_bugs'],
                           blocker_bugs_url=bugs['blocker_bugs_url'],
                           )


@main_blueprint.route("/packages/<package_name>/problems")
def package_problems(package_name):
    return render_template("main/package-problems.html",
                           package_name=package_name)


@main_blueprint.route("/packages/<package_name>/contents")
def package_contents(package_name):
    return render_template("main/package-contents.html",
                           package_name=package_name)


@cache.cached(timeout=600)
@main_blueprint.route("/packages/<package_name>/changelog")
def package_changelog(package_name):
    changelog = get_changelogs(package_name)
    return render_template("main/package-changelog.html",
                           package_name=package_name,
                           changelog=changelog)


@main_blueprint.route("/packages/<package_name>/sources")
def package_sources(package_name):
    return render_template("main/package-sources.html",
                           package_name=package_name)
