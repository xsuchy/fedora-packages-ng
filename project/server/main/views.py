# project/server/main/views.py


from flask import render_template, Blueprint


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
        return render_template("main/package-overview.html", package_name=package_name)

@main_blueprint.route("/packages/<package_name>/builds")
def package_builds(package_name):
    return render_template("main/package-builds.html", package_name=package_name)

