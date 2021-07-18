import logging
from typing import List, Tuple, Dict

import psycopg2

from tools.utils import read_config


class Postgres:
    def __init__(self, config: Dict = None):
        self.connection = None
        self.cursor = None
        self.connect(config)

    def connect(self, config: Dict = None) -> None:
        config = config or read_config()
        pg_con_params = config.get('postgresql')
        assert pg_con_params
        self.connection = psycopg2.connect(**pg_con_params)
        logging.info("Database connect established")
        self.cursor = self.connection.cursor()

    def execute(self, req: str) -> None:
        self.cursor.execute(req)

    def fetch_data(self) -> List[Tuple]:
        return self.cursor.fetchall()

    def commit(self) -> None:
        self.connection.commit()

    def exec_file(self, filepath: str):
        with open(filepath, 'r') as f:
            self.cursor.execute(f.read())



