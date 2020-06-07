import requests
from urllib.parse import urlencode
from .models import DatagrepperMessage


DATAGREPPER = "https://apps.fedoraproject.org/datagrepper/raw"


def send_request(params):
    url = DATAGREPPER + "?" + urlencode(params)
    return requests.get(url).json()


def get_recent_history(package_name):
    params = {
        "order": "desc",
        "meta": ["subtitle", "link", "icon", "secondary_icon"],
        "package": package_name,
        "grouped": True,
        "not_topic": [
            "org.fedoraproject.prod.buildsys.rpm.sign",
            "org.fedoraproject.prod.buildsys.tag",
            "org.fedoraproject.prod.buildsys.untag",
            "org.fedoraproject.prod.buildsys.package.list.change",
        ],
        "rows_per_page": 20,
    }
    response = send_request(params)
    return [DatagrepperMessage(m) for m in response["raw_messages"]]
