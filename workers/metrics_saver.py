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
        self._execute(req)
        self.connection.commit()

    def save(self, payload: Dict) -> None:
        hostname = payload.pop("hostname")
        kv = [(k, v) for k, v in payload.items()]
        self.insert_line(hostname, [k for k, _ in kv], [v for _, v in kv])
        self.connection.commit()

    def prepare(self, tables: List[str]) -> None:
        for table in tables:
            self.create_table(table)

    def drop_table(self, table: str):
        req = f"DROP TABLE {table};"
        self._execute(req)