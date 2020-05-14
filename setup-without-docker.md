# Setup

Use this guide if you do NOT want to use Docker in your project.

## Getting Started

Create and activate a virtual environment, and then install the requirements.

### Set Environment Variables

Update *fedoracommunity/server/config.py*, and then run:

```sh
$ export APP_NAME="fedora-packages"
$ export APP_SETTINGS="fedoracommunity.server.config.ProductionConfig"
$ export FLASK_DEBUG=0
```
By default the app is set to use the production configuration. If you would like to use the development configuration, you can alter the `APP_SETTINGS` environment variable:

```sh
$ export APP_SETTINGS="fedoracommunity.server.config.DevelopmentConfig"
```

Using [Pipenv](https://docs.pipenv.org/) or [python-dotenv](https://github.com/theskumar/python-dotenv)? Use the *.env* file to set environment variables:

```
APP_NAME="fedora-packages"
APP_SETTINGS="fedoracommunity.server.config.DevelopmentConfig"
FLASK_DEBUG=1
```

### Install dependencies

See [Dockerfile](./Dockerfile) - Required dependencies part to install the nesssary RPMs.

### Create DB

```sh
$ python3 manage.py create-db
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py create-data
```

### Run the Application


```sh
$ python3 manage.py run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

### Testing

Without coverage:

```sh
$ python3 manage.py test
```

With coverage:

```sh
$ python3 manage.py cov
```

Run flake8 on the app:

```sh
$ python3 manage.py flake
```

or

```sh
$ flake8 project
```
