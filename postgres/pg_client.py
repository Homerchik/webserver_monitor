import yaml
from typing import List

import psycopg2


class Postgres:
    def __int__(self):
        self.connection = None

    def connect(self):
        with open('configs/config.yaml', 'r') as f:
            pg_con_params = yaml.safe_load(f)
            assert pg_con_params
            return psycopg2.connect(**pg_con_params.get('postgres'))

    def execute(self):
        pass


def insert_req(table: str, fields: List[str], values: List) -> str:
    return f"INSERT INTO {table}({fields}) values({values})"
