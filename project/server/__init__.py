import datetime
import os

import flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import humanize

# instantiate the extensions
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app(script_info=None):

    # instantiate the app
    app = flask.Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv(
        "APP_SETTINGS", "project.server.config.ProductionConfig"
    )
    app.config.from_object(app_settings)

    # set up extensions
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.server.main.views import main_blueprint

    app.register_blueprint(main_blueprint)

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return flask.render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return flask.render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return flask.render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return flask.render_template("errors/500.html"), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    # Serve static files from system-wide RPM files
    @app.route('/system_static/<component>/<path:filename>')
    @app.route('/system_static/<path:filename>')
    def system_static(filename, component=""):
        """
        :param component: name of the javascript component provided by a RPM
                          package do not confuse with a name of the RPM
                          package itself (e.g. 'jquery' component is provided
                          by 'js-jquery1' package)
        :param filename: path to a file relative to the component root
                         directory
        :return: content of a static file
        """
        path = os.path.join("/usr/share/javascript", component)
        return flask.send_from_directory(path, filename)

    @app.template_filter('time_ago')
    def time_ago(time_in, until=None):
        """ returns string saying how long ago the time on input was

        Input is in EPOCH (seconds since epoch).
        """
        if time_in is None:
            return " - "
        if until is not None:
            now = datetime.datetime.fromtimestamp(until)
        else:
            now = datetime.datetime.now()
        diff = now - datetime.datetime.fromtimestamp(time_in)
        return humanize.naturaldelta(diff)

# continuation of block of create_app()
    return app
# END of create_app()


app = create_app()
