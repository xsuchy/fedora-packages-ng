from .models import Package


# @TODO have some real logic function for this
def get_packages():
    return [
        Package("pkg1", "sum1", [Package("sub1", "subsum1"), Package("sub2", "subsum2")]),
        Package("pkg2", "sum2", [Package("sub3", "subsum3")]),
    ]


# @TODO have some real logic function for this
def get_package(package_name):
    return Package(package_name, "Summary for {0} package".format(package_name))
