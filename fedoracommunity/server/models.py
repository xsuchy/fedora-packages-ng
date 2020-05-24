# fedoracommunity/server/models.py

class Package:
    def __init__(self, name, summary, subpackages=None):
        self.name = name
        self.summary = summary
        self.subpackages = subpackages

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
