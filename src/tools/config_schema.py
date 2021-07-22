from typing import Dict


def schema(service_type: str) -> Dict:
    if service_type == "consumer":
        return {"postgresql": {"host": "", "port": "", "user": "", "password": "", "dbname": ""},
                "kafka": {"bootstrap_servers": ""},
                "kafka_cons": {"auto_offset_reset": ""},
                "application": {"chunk_size": ""},
                "monitoring": ""}
    elif service_type == "producer":
        return {"kafka": {"bootstrap_servers": ""},
                "application": {"update_interval": ""},
                "monitoring": ""}
