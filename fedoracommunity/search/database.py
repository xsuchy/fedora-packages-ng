import json
import urllib
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
        queryparser.set_database(self.db)
        enquire = xapian.Enquire(self.db)

        flags = xapian.QueryParser.FLAG_DEFAULT | \
            xapian.QueryParser.FLAG_PARTIAL | \
            xapian.QueryParser.FLAG_WILDCARD

        fulltext_querystring = self._fulletxt_search_string(querystring)
        query = queryparser.parse_query(fulltext_querystring, flags)
        enquire.set_query(query)
        return Query(enquire.get_mset(offset, pagesize))

    def search_one(self, querystring):
        """
        Search for one result that has the exact match for `querystring`
        and return `Query` object.
        """
        search_name = self._filter_search_string(querystring)
        search_string = "%s EX__%s__EX" % (search_name, search_name)

        matches = self.search(search_string).all()
        if len(matches) == 0:
            return None

        # Sometimes (rarely), the first match is not the one we actually want.
        for match in matches:
            if match["name"] == querystring:
                return match
            if any([sp["name"] == querystring for sp in match["sub_pkgs"]]):
                return match
        return None

    def _filter_search_string(self, string):
        """
        Replaces xapian reserved characters with underscore, lowercases
        the string and replaces spelling of certain words/names with more
        common versions

        Reserved Characters:
            +, -, ', "
        """
        reserved_chars = ["+", "-", "\\", "\""]
        words_translation = {"d-bus": "dbus", "gtk+": "gtk"}

        string = string.lower()
        for key, value in words_translation.items():
            string = string.replace(key, value)

        for char in reserved_chars:
            string = string.replace(char, "_")
        return string

    def _fulletxt_search_string(self, querystring):
        search_string = urllib.parse.unquote_plus(querystring)
        search_string = self._filter_search_string(search_string)
        phrase = '"%s"' % search_string

        # add exact matchs
        search_terms = search_string.split(' ')
        search_terms = [t.strip() for t in search_terms if t.strip()]
        for term in search_terms:
            search_string += " EX__%s__EX" % term

        # add phrase match
        search_string += " OR %s" % phrase

        if len(search_terms) > 1:
            # add near phrase match (phrases that are near each other)
            search_string += " OR (%s)" % ' NEAR '.join(search_terms)

        # Add partial/wildcard matches
        search_string += " OR (%s)" % ' OR '.join([
            "*%s*" % term for term in search_terms])

        return search_string


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
