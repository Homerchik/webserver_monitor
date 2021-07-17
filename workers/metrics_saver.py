import logging
from typing import List, Dict

from interfaces.storage import Storage
from wrappers.postgres import Postgres


class PostgresMetrics(Postgres, Storage):
    mappings = {"ts": int, "page": str, "status": int, "latency": int, "regex_valid": bool}

    def insert_line(self, table: str, fields: List[str], values: List):
        v = [f"'{vv}'" if self.mappings.get(f) == str else str(vv) for f, vv in zip(fields, values)]
        req = f"INSERT INTO {table}({','.join(fields)}) values({', '.join(v)})"
        self._execute(req)

    def create_table(self, table: str):
        req = f"CREATE TABLE IF NOT EXISTS {table} " \
              f"(ts BIGINT NOT NULL," \
              f"page VARCHAR(255), status INTEGER NOT NULL, latency BIGINT NOT NULL, " \
              f"regex_valid BOOLEAN NOT NULL);"
        try:
            self._execute(req)
            self.connection.commit()
            logging.info(f"Table {table} created successfully")
        except Exception as e:
            logging.error(f"Table {table} creation failed due to {e}")
            raise e

    def tables_list_in_db(self):
        req = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        try:
            self._execute(req)
            tables = [table for table, *_ in self.cursor.fetchall()]
            return tables
        except Exception as e:
            logging.error(f"Tables list request failed with {e}")
            raise e

    def save(self, payload: Dict) -> None:
        hostname = payload.pop("hostname")
        kv = [(k, v) for k, v in payload.items()]
        try:
            self.insert_line(hostname, [k for k, _ in kv], [v for _, v in kv])
            self.connection.commit()
            logging.debug("Insert successful")
        except Exception as e:
            logging.error(f"Insert failed due to {e}")
            raise e

    def prepare(self, tables: List[str]) -> None:
        tables_in_db = self.tables_list_in_db()
        for table in tables:
            if table not in tables_in_db:
                self.create_table(table)

    def drop_table(self, table: str):
        req = f"DROP TABLE {table};"
        self._execute(req)
        self.connection.commit()