from parser import Page
import json
import psycopg2
from contextlib import closing


class DataBaseAdaptor:
    def __init__(self, db_dict: dict):
        self.save_path = '/home/vh/VHFind/Crawler/save/'
        self.db = db_dict['db']
        self.user = db_dict['user']
        self.password = db_dict['password']
        self.host = db_dict['host']

    def save_content(self, number: int, page: Page):
        """Save page content to data index"""
        with open(self.save_path + str(number) + '.txt', 'w') as file:
            file.write(json.dumps(page.tokenized_content))

    def test_execute(self):
        """Version dn"""
        with closing(self.get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT version()')
                print(cursor.fetch_one())

    def get_connection(self):
        """connection factory"""
        return psycopg2.connect(
            dbname=self.db,
            user=self.user,
            password=self.password,
            host=self.host
        )
