import requests
from urllib.parse import urlencode
from paste.httpexceptions import HTTPBadGateway


RETRACE = "https://retrace.fedoraproject.org/faf/problems"


def get_problems(package_name):
    params = {"component_names": package_name}
    url = RETRACE + "?" + urlencode(params)
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code != requests.codes['ok']:
        msg = "Failed to talk to retrace server, {0} {1}".format(url, response)
        raise HTTPBadGateway(msg)
    return response.json()['problems']
