import requests
import logging
from datetime import datetime, timezone

import json

class ELKHandler(logging.Handler):
    def __init__(self, elasticsearch_url, index):
        super().__init__()
        self.elasticsearch_url = elasticsearch_url
        self.index = index

    def emit(self, record):
        log_entry = self.format(record)
        print(log_entry)
        url = f"{self.elasticsearch_url}/{self.index}/_doc/"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, data=log_entry)
            if response.status_code not in [200, 201]:
                self.handleError(record)
        except Exception as e:
            self.handleError(record)

    def format(self, record):
        value = getattr(record, 'value', None)
        if value != None:
            value = int(value)
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": record.getMessage(),
            "loglevel": record.levelname,
            "status": getattr(record, 'status', None),
            "operation": getattr(record, 'operation', None),
            "value": value
        }
        return json.dumps(log_entry)