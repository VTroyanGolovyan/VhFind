import psycopg2
from contextlib import closing


class DataBaseAdaptor:
    def __init__(self, db_dict: dict):
        self.db = db_dict["db"]
        self.user = db_dict["user"]
        self.password = db_dict["password"]
        self.host = db_dict["host"]

    def sign_up(
            self,
            name,
            last_name,
            login,
            password
    ):
        """Sign up function"""
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
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

    def get_connection(self):
        """connection factory"""
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host
        )
