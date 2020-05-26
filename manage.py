# manage.py


import unittest

import coverage

from flask.cli import FlaskGroup

from fedoracommunity.server import app, db
import subprocess
import sys

def create_app():
    return app

cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include="fedoracommunity/*",
    omit=[
        "fedoracommunity/tests/*",
        "fedoracommunity/server/config.py",
        "fedoracommunity/server/*/__init__.py",
    ],
)
COV.start()


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_data():
    """Creates sample data."""
    pass


@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def flake():
    """Runs flake8 on the project."""
    process = subprocess.run(["flake8", "project"])
    if process.returncode == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    cli()
