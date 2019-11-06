import urllib
from bugzilla import RHBugzilla as Bugzilla

PRODUCTS = ['Fedora', 'Fedora EPEL', 'Fedora Modules']

# Don't query closed bugs for these packages, since the queries timeout
BLACKLIST = ['kernel']

MAX_BZ_QUERIES = 200
BUG_SORT_KEYS = ['status', 'product', 'version', 'bug_id']

OPEN_BUG_STATUS = ['__open__']

URL = "https://bugzilla.redhat.com/xmlrpc.cgi"

COLLECTION = ['Fedora', 'Fedora EPEL']

LARGE = 10000

# We want items to appear by status in a certain order, not
# alphabetically.  Items I forgot to hardcode just go last.
STATUS_ORDER = ['NEW', 'VERIFIED', 'ASSIGNED', 'MODIFIED',
                'ON_DEV', 'ON_QA', 'RELEASE_PENDING', 'POST']


def _open_bugs(bugzilla_client, package_name):
    query = bugzilla_client.build_query(product=COLLECTION,
                                        component=package_name,
                                        status=OPEN_BUG_STATUS,
                                        )
    return bugzilla_client.query(query)


def blocker_bugs(open_bugs):
    result = set()
    for b in open_bugs:
        if b.blocks:
            result = result.union(b.blocks)
    return result


def _version_to_int(val):
    try:
        return -1 * int(val[0])
    except (ValueError, IndexError):
        return -1 * LARGE


def _status_to_index(val):
    try:
        return STATUS_ORDER.index(val)
    except ValueError:
        return len(STATUS_ORDER)


def get_bugs(package_name):
    bugzilla_client = Bugzilla(url=URL,
                               cookiefile=None, tokenfile=None)

    bugs = _open_bugs(bugzilla_client, package_name)
    blocker_bugs_results = blocker_bugs(bugs)
    results = {'bugs': [],
               'open_bugs': len(bugs),
               'blocker_bugs': len(blocker_bugs_results),
               }
    # Generate the URL for the blocker bugs
    url_args = [
        ('classification', 'Fedora'),
        ('query_format', 'advanced'),
        ('component', package_name),
    ]
    for product in PRODUCTS:
        url_args.append(('product', product))
    for status in OPEN_BUG_STATUS:
        url_args.append(('bug_status', status))

    results['open_bugs_url'] = "https://bugzilla.redhat.com/buglist.cgi?" + \
                               urllib.parse.urlencode(url_args)
    url_args += [
        ('f1', 'blocked'),
        ('o1', 'anywordssubstr'),
        ('v1', ' '.join(map(str, blocker_bugs_results))),
    ]
    results['blocker_bugs_url'] = \
        "https://bugzilla.redhat.com/buglist.cgi?" + \
        urllib.parse.urlencode(url_args)
    for fb in bugs:
        bug_version = fb.version
        if isinstance(bug_version, (list, tuple)):
            bug_version = bug_version[0]
        results['bugs'].append({'id': fb.bug_id,
                                'status': fb.bug_status.title(),
                                'summary': fb.summary,
                                'release': '{} {}'.format(fb.product,
                                                          bug_version),
                                'version_sort': _version_to_int(fb.version),
                                'status_sort': _status_to_index(fb.bug_status),
                                })
    return results
