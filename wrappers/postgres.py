import logging

import psycopg2

from tools.utils import read_config


class Postgres:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        config = read_config()
        pg_con_params = config.get('postgresql')
        assert pg_con_params
        self.connection = psycopg2.connect(**pg_con_params)
        logging.info("Database connect established")
        self.cursor = self.connection.cursor()

    def _execute(self, req: str):
        self.cursor.execute(req)

    def exec_file(self, filepath: str):
        with open(filepath, 'r') as f:
            self.cursor.execute(f.read())



