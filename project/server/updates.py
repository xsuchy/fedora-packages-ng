import bodhi.client.bindings
import datetime


def _get_age(date):
    if date:
        return datetime.datetime.fromisoformat(date).timestamp()
    else:
        return None


def get_updates(package_name):
    bodhi_client = bodhi.client.bindings.BodhiClient()
    # releases = bodhi_client.get_releases().releases
    # releases = [v for v in releases if v.state != "archived"]
    updates = []
    fetched_updates = bodhi_client.query(packages=package_name)
    for fu in fetched_updates.updates:
        updates.append({'version': fu.title,
                        'age': _get_age(fu.date_pushed),
                        'status': fu.status,
                        'link': fu.url,
                        'date_pushed': fu.date_pushed,
                        'karma': fu.karma,
                        'updateid': fu.updateid,
                        'request': fu.request,
                       }
                      )
    return updates

