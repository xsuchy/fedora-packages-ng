from datetime import datetime

import os
import re
import requests
from urllib.parse import urljoin
from paste.httpexceptions import HTTPBadGateway

MDAPI_URL = "https://mdapi.fedoraproject.org/"


def get_contents(package_name, release="rawhide"):
    url = '/'.join([MDAPI_URL, release, 'files', package_name])
    response = requests.get(url)
    if not bool(response):
        raise HTTPBadGateway("Failed to talk to mdapi, %r %r" % (
                             url, response))
    data = response.json()
    if 'files' in data:
        data = data['files']
    else:
        # IMPOSSIBLE!
        raise HTTPBadGateway("Got unexpected response from mdapi.")

    files = []
    for item in data:
        for filename in item["filenames"].split("/"):
            # import ipdb; ipdb.set_trace()
            files.append(os.path.join(item["dirname"], filename))
    return files
