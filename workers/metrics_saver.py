import logging
from typing import List, Dict

from interfaces.storage import Storage
from wrappers.postgres import Postgres


class PostgresMetrics(Postgres, Storage):
    def __init__(self, config: Dict = None):
        super().__init__(config=config)

    mappings = {"ts": int, "page": str, "status": int, "latency": int, "regex_valid": bool}

    @staticmethod
    def insert_line(table: str, fields: List[str], values: List) -> str:
        v = [f"'{vv}'" if PostgresMetrics.mappings.get(f) == str else str(vv) for f, vv in zip(fields, values)]
        return f"INSERT INTO {table}({', '.join(fields)}) values({', '.join(v)})"

    def create_table(self, table: str):
        req = f"CREATE TABLE IF NOT EXISTS {table} " \
              f"(ts BIGINT NOT NULL," \
              f"page VARCHAR(255), status INTEGER NOT NULL, latency BIGINT NOT NULL, " \
              f"regex_valid BOOLEAN NOT NULL);"
        try:
            self.execute(req)
            self.commit()
            logging.info(f"Table {table} created successfully")
        except Exception as e:
            logging.error(f"Table {table} creation failed due to {e}")
            raise e

    def tables_list_in_db(self):
        req = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        try:
            self.execute(req)
            tables = [table for table, *_ in self.cursor.fetchall()]
            return tables
        except Exception as e:
            logging.error(f"Tables list request failed with {e}")
            raise e

    def save(self, payload: Dict) -> None:
        try:
            for item in payload:
                hostname = item.pop("hostname")
                kv = [(k, v) for k, v in item.items()]
                line = self.insert_line(hostname, [k for k, _ in kv], [v for _, v in kv])
                self.execute(line)
            self.connection.commit()
            logging.debug(f"Insert of {len(payload)} records was successful")
        except Exception as e:
            logging.error(f"Insert failed due to {e}")

    def prepare(self, tables: List[str]) -> None:
        tables_in_db = self.tables_list_in_db()
        for table in tables:
            if table not in tables_in_db:
                self.create_table(table)

    def drop_table(self, table: str):
        req = f"DROP TABLE {table};"
        self.execute(req)
        self.commit()