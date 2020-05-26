import json
import xapian


class Database:
    """
    This is a high-level facade over the xapian cache.

    The main goal is to abstract its user from even knowing that he works with
    xapian and rather provide a simple interface for searching values as well as
    inserting, updating and deleting them.
    """

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.db = xapian.Database(dbpath)

    def search(self, querystring, offset=0, pagesize=10):
        """
        Search `querystring` in xapian database and return `Query` object.

        For more information about xapain searching, see:
        https://getting-started-with-xapian.readthedocs.io/en/latest/practical_example/searching/building.html
        """
        queryparser = xapian.QueryParser()
        query = queryparser.parse_query(querystring)
        enquire = xapian.Enquire(self.db)
        enquire.set_query(query)
        return Query(enquire.get_mset(offset, pagesize))

    def search_one(self, querystring):
        """
        Search for one result that has the exact match for `querystring`
        and return `Query` object.
        """
        # @TODO more inteligent search and exact strict matching
        return self.search(querystring, pagesize=1)


class Query:
    """
    A result of every `Database` search is a `Query` object.

    It allows you (@TODO) to access additional pages of results
    as well as map a model over the results.
    """

    def __init__(self, xapian_mset):
        self.xapian_mset = xapian_mset
        self.model = None

    def all(self):
        results = []
        for match in self.xapian_mset:
            result = json.loads(match.document.get_data())
            results.append(self._to_model(result))
        return results

    def count(self):
        return self.xapian_mset.get_matches_estimated()

    def _to_model(self, result):
        if self.model:
            return self.model(result)
        return result
