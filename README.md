# fedora-packages

[![Build Status](https://travis-ci.org/xsuchy/fedora-packages-ng.svg?branch=master)](https://travis-ci.org/xsuchy/fedora-packages-ng)

Fedora Packages Next Generation version replacing [Fedora Packages](https://apps.fedoraproject.org/packages/) ([source](https://github.com/fedora-infra/fedora-packages)).

## Quick Start

```sh
$ docker-compose up --build
```

Then access to [the top page](http://127.0.0.1:5002) and [the package page](http://127.0.0.1:5002/packages/python3).

Review the set up guides to configure the app for detail:

1. [setup-with-docker.md](setup-with-docker.md)
2. [setup-without-docker.md](setup-without-docker.md)

## Get the data

You can run:

./index-packages --debug -p /tmp/ --index-db-dest index-db
