from parser import Page
import psycopg2
from contextlib import closing


class DataBaseAdaptor:
    def __init__(self, db_dict: dict):
        self.db = db_dict["db"]
        self.user = db_dict["user"]
        self.password = db_dict["password"]
        self.host = db_dict["host"]

    def save_content(self, page: Page):
        """Save page content to data index"""
        site_id = self._detect_and_insert_site(page)
        lang_id = self._get_language_id(page)
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO urls (url, site, lang, title, visitors, from_nav, quotation, doc_length) "
                    " VALUES (%(url)s, %(site_id)s, %(lang_id)s, %(title)s, 0, FALSE, 0, %(doc_len)s) "
                    " RETURNING id ",
                    {
                        "url": page.url,
                        "lang_id": lang_id,
                        "title": page.title,
                        "doc_len": page.doc_length,
                        "site_id": site_id
                    }
                )
                page.set_id(int(cursor.fetchone()[0]))
                conn.commit()
        self._save_tokens(page)
        self._make_many_to_many_relationship(page)

    def test_execute(self):
        """DB Version"""
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version()")

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
                        conn.commit()
            except Exception as e:
                print(e)

    def _make_many_to_many_relationship(self, page: Page):
        """Makes many to many relations between urls and tokens"""
        tokens = page.get_counted_tokens()
        for position, token in enumerate(page.tokenized_content):
            try:
                with closing(self.get_connection()) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "SELECT id FROM tokens WHERE token=%(token)s LIMIT 1",
                            {
                                "token": token.text
                            }
                        )
                        token_id = cursor.fetchone()[0]
                        cursor.execute(
                            "INSERT INTO urls_tokens (url, token, tf, token_position) "
                            " VALUES "
                            "   (%(url_id)s, %(token_id)s, %(tf)s, %(token_position)s)",
                            {
                                "url_id": page.id,
                                "token_id": token_id,
                                "tf": tokens[token],
                                "token_position": position
                            }
                        )
                        conn.commit()
            except Exception as e:
                print(e)

    def _get_language_id(self, page: Page):
        try:
            with closing(self.get_connection()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO languages (lang_name) "
                        " VALUES (%(lang_name)s) "
                        "ON CONFLICT (lang_name) "
                        " DO NOTHING ",
                        {
                            "lang_name": page.lang
                        }
                    )
                    cursor.execute(
                        "SELECT id FROM languages WHERE lang_name=%(lang_name)s",
                        {
                            "lang_name": page.lang
                        }
                    )
                    lang_id = cursor.fetchone()[0]
                    conn.commit()
                    return lang_id
        except Exception:
            return 0

    def _detect_and_insert_site(self, page: Page):
        try:
            with closing(self.get_connection()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO sites (url, subdomain) "
                        " VALUES (%(url)s, 0) "
                        "ON CONFLICT (url) "
                        " DO NOTHING ",
                        {
                            "url": page.domain
                        }
                    )
                    cursor.execute(
                        "SELECT id FROM sites WHERE url=%(url)s",
                        {
                            "url": page.domain
                        }
                    )
                    site_id = cursor.fetchone()[0]
                    conn.commit()
                    return site_id
        except Exception:
            return 0

    def get_connection(self):
        """connection factory"""
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host
        )
