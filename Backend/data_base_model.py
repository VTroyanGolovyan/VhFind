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
            condition = ' OR '.join(["tokens.token LIKE '%" + token.lower() + "%'" for token in query_tokens])
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT urls.url, urls.title, "
                    " sum(log((SELECT COUNT(*) FROM urls) / (tokens.idf + 1)) * ut.tf) "
                    " as relevance, urls.id FROM tokens "
                    "inner join urls_tokens as ut on tokens.id = ut.token "
                    "inner join urls on ut.url = urls.id WHERE " + condition + " GROUP BY urls.id "
                                                                               " ORDER BY relevance DESC LIMIT 20"
                )
                return [(el[0], el[1], float(el[2]), self.restore_url_content(el[3])) for el in cursor]

    def restore_url_content(self, id):
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT tokens.token, urls_tokens.token_position FROM urls_tokens "
                    "JOIN tokens on tokens.id=urls_tokens.token "
                    "WHERE urls_tokens.url=%(url)s ORDER BY urls_tokens.token_position LIMIT 50 OFFSET 450",
                    {
                        "url": id
                    }
                )
                return ' '.join([token[0] for token in cursor])

    def sign_up(
        self,
        name,
        last_name,
        email,
        age,
        pass_hash,
        salt
    ):
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, last_name, email, password, age, confirmation_hash, salt) "
                    "VALUES (%(name)s, %(last_name)s, %(email)s, %(password)s, %(age)s, %(confirmation_hash)s, %(salt)s) "
                    "RETURNING id",
                    {
                        'name': name,
                        'last_name': last_name,
                        'email': email,
                        'password': pass_hash,
                        'age': age,
                        'confirmation_hash': 'soon',
                        'salt': salt
                    }
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                return user_id

    def get_by_email(self, email):
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, email, password, salt FROM users "
                    "WHERE email=%(email)s LIMIT 1",
                    {
                        "email": email
                    }
                )

                user = cursor.fetchone()
                conn.commit()
                return user[0], user[1], user[2], user[3]

    def new_session(self, user, token):
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sessions (user_id, token) "
                    " VALUES (%(user)s, %(token)s)",
                    {
                        "user": user,
                        "token": token
                    }
                )
                conn.commit()
                return token

    def get_user_by_token(self, token):
        try:
            with closing(self.get_connection()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT user FROM sessions"
                        " WHERE token=%(token)s",
                        {
                            "token": token
                        }
                    )
                    uid = cursor.fetchone()[0]
                    conn.commit()
                    return uid
        except Exception as e:
            return 0

    def get_connection(self):
        """connection factory"""
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host
        )
