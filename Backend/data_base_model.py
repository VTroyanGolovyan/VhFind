import psycopg2
from contextlib import closing


class DataBaseAdaptor:
    def __init__(self, db_dict: dict):
        self.db = db_dict["db"]
        self.user = db_dict["user"]
        self.password = db_dict["password"]
        self.host = db_dict["host"]

    def find_query(self, query_tokens):
        with closing(self.get_connection()) as conn:
            condition = ' OR '.join(["tokens.token='"+ token.lower() + "'" for token in query_tokens])
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT DISTINCT urls.url, urls.title FROM tokens "
                    "inner join urls_tokens as ut on tokens.id = ut.token "
                    "inner join urls on ut.url = urls.id WHERE " + condition
                )
                return [(el[0], el[1]) for el in cursor]

    def get_connection(self):
        """connection factory"""
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host
        )
