import yaml

import psycopg2


class Postgres:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        with open('../configs/config.yaml', 'r') as f:
            pg_con_params = yaml.safe_load(f)
            assert pg_con_params
            self.connection = psycopg2.connect(**pg_con_params.get('postgresql'))
            self.cursor = self.connection.cursor()

    def _execute(self, req: str):
        self.cursor.execute(req)

    def exec_file(self, filepath: str):
        with open(filepath, 'r') as f:
            self.cursor.execute(f.read())



