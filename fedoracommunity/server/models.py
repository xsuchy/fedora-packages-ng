# fedoracommunity/server/models.py

class Package:
    def __init__(self, xapian_dict):
        self._xapian_dict = xapian_dict

        # Required values
        self.name = xapian_dict["name"]
        self.summary = xapian_dict["summary"]
        self.description = xapian_dict["description"]

        # Optional values
        self.homepage = xapian_dict.get("upstream_url")
        self.owner = xapian_dict.get("devel_owner")
        self.subpackages = [Package(x) for x in xapian_dict.get("sub_pkgs", [])]

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
