# fedoracommunity/server/models.py

class Package:
    def __init__(self, name, summary, subpackages=None):
        self.name = name
        self.summary = summary
        self.subpackages = subpackages

        # TODO
        self.description = "This is a description for {0} package".format(name)
        self.homepage = "https://foo.bar/baz"
        self.owner = Owner("msuchy")

    @property
    def url(self):
        return "/packages/" + self.name

    @property
    def parent(self):
        # @TODO proper implementation
        return Package("pkg1", "sum1")

    @property
    def is_subpackage(self):
        # @TODO proper implementation
        return self.name.startswith("sub")

    @property
    def latest_build(self):
        # @TODO proper implementation
        return "123-1.fc33"


class Owner:
    def __init__(self, name):
        self.name = name

    @property
    def url(self):
        if self.name.endswith("-maint"):
            return "https://admin.fedoraproject.org/pkgdb/users/packages/{0}".format(self.name)
        return "https://fedoraproject.org/wiki/User:{0}".format(self.name)
