from datetime import datetime

import re
import requests
import urllib.parse
from paste.httpexceptions import HTTPBadGateway

MDAPI_URL = "https://mdapi.fedoraproject.org/"
_changelog_version_extract_re = re.compile(r'(.*)\W*<(.*)>\W*-?\W*(.*)')


def get_changelogs(package_name):
    url = urllib.parse.urljoin(MDAPI_URL,
                               'rawhide/changelog/{}'.format(package_name))
    response = requests.get(url)
    if not bool(response):
        raise HTTPBadGateway("Failed to talk to mdapi, %r %r" % (
                             url, response))
    data = response.json()
    if 'changelogs' in data:
        data = data['changelogs']
    else:
        # IMPOSSIBLE!
        raise HTTPBadGateway("Got unexpected response from mdapi.")

    for i, entry in enumerate(data):
        entry['text'] = entry['changelog']
        m = _changelog_version_extract_re.match(entry['author'])
        if m:
            entry['author'] = m.group(1)
            entry['email'] = m.group(2)
            entry['version'] = m.group(3)
        else:
            entry['author'] = entry['author']
        entry['date'] = datetime.fromtimestamp(entry['date'])
    return data
