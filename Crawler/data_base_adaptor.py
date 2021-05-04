from parser import Page
import psycopg2
from contextlib import closing


class DataBaseAdaptor:
    def __init__(self, db_dict: dict):
        self.db = db_dict['db']
        self.user = db_dict['user']
        self.password = db_dict['password']
        self.host = db_dict['host']

    def save_content(self, page: Page):
        """Save page content to data index"""
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO urls (url, site, lang, title, visitors, from_nav, quotation) "
                    " VALUES (%(url)s, 0, 0, %(title)s, 0, FALSE, 0)",
                    {
                        "url": page.url,
                        "title": page.title
                    }
                )
                conn.commit()
        self._save_tokens(page)

    def test_execute(self):
        """DB Version"""
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT version()')

    def _save_tokens(self, page: Page):
        tokens = page.get_counted_tokens()
        for token in tokens.keys():
            try:
                with closing(self.get_connection()) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO tokens (token, idf, lang, metaphone) "
                            " VALUES (%(token)s, 1, 0, %(metaph)s)"
                            "ON CONFLICT (token) "
                            "DO "
                            "   UPDATE SET idf = tokens.idf + 1",
                            {
                                "token": token.text,
                                "metaph": token.metaphone
                            }
                        )
                        print(token.lang + ' ' + token.text)
                        conn.commit()
            except Exception as e:
                print(e)

    def get_connection(self):
        """connection factory"""
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host
        )
