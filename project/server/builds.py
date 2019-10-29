import koji


def get_builds(package_name):
    koji_client = koji.ClientSession('https://koji.fedoraproject.org/kojihub')

    pkg_id = None
    if package_name:
        pkg_id = koji_client.getPackageID(package_name)

    fetched_builds = koji_client.listBuilds(packageID=pkg_id,
                                            # state=state,
                                            completeBefore=None,
                                            completeAfter=None,
                                            queryOpts={})

    builds = []
    for fb in fetched_builds:
        builds.append({'build_id': fb['build_id'],
                       'nvr': fb['nvr'],
                       'creation': fb['creation_ts'],
                       'completion': fb['completion_ts'],
                       'owner_name': fb['owner_name'],
                       'state': str(fb['state']),
                       })
    return builds
