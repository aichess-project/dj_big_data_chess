import logging
import sys
import requests

from datetime import datetime, timezone
import json
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

# Configuration
log_level = logging.INFO
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

file_logging = {
    "enabled": True,
    "filename": "app.log",
    "max_file_size": 5242880,  # 5 MB
    "backup_count": 5
}

elk_logging = {
    "enabled": True,
    "logstash_url": "http://localhost:5000",
    "index": "log_big_data_chess"
}

class LogJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, log_format, *args, **kwargs):
        # Define the log message format you want
        super(LogJsonFormatter, self).__init__(fmt=log_format, *args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super(LogJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        log_record['level'] = record.levelname
        log_record['logger_name'] = record.name
        log_record['status'] = record.__dict__.get('status', None)
        log_record['function'] = record.__dict__.get('function', None)
        log_record['variable'] = record.__dict__.get('variable', None)
        log_record['value'] = record.__dict__.get('value', None)

class ELKHandler(logging.Handler):
    def __init__(self, log_format, elk_url, elk_index):
        super().__init__()
        self.elk_url = elk_url
        self.elk_index = elk_index
        self.formatter = LogJsonFormatter(log_format=log_format)

    def emit(self, record):
        log_message = self.format(record)
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(f"{self.elk_url}/{self.elk_index}", headers=headers, data=log_message)
            if response.status_code != 200:
                self.handleError(record)
        except Exception as e:
            self.handleError(record)

class ELK_Logger:
    def __init__(self, log_level = log_level, log_format = log_format, file_logging = file_logging, elk_logging = elk_logging):
        self.logger = logging.getLogger(__name__)  # Initialize the logger
        self.formatter = LogJsonFormatter(log_format=log_format)
        self._configure_logger(log_level, file_logging, elk_logging)

    def _configure_logger(self, log_level, file_logging, elk_logging):
        # Set logging level
        self.logger.setLevel(log_level)

        # Configure file logging
        if file_logging["enabled"] == True:
            file_handler = RotatingFileHandler(
                file_logging["filename"],
                maxBytes=file_logging["max_file_size"],
                backupCount=file_logging["backup_count"]
            )
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

        # Configure ELK/Logstash logging if configured
        if elk_logging['enabled'] == "True":
            elk_url = elk_logging['logstash_url']
            elk_index = elk_logging['index']
            if elk_url:
                elk_handler = ELKHandler(self.formatter, elk_url, elk_index)
                elk_handler.setLevel(log_level)
                elk_handler.setFormatter(self.formatter)
                self.logger.addHandler(elk_handler)

    def log(self, level, message: str, status: str = None, function = None, variable: str = None, value = None):
        extra = {
            'status': status,
            'function': function,
            'variable': variable,
            'value': value
        }
        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, status = None, function = None, variable = None, value = None):
        self.log(logging.DEBUG, message, status, function, variable, value)

    def info(self, message: str, status = None, function = None, variable = None, value = None):
        self.log(logging.INFO, message, status, function, variable, value)

    def warning(self, message: str, status = None, function = None, variable = None, value = None):
        self.log(logging.WARNING, message, status, function, variable, value)

    def error(self, message: str, status = None, function = None, variable = None, value = None):
        self.log(logging.ERROR, message, status, function, variable, value)

    def critical(self, message: str, status = None, function = None, variable = None, value = None):
        self.log(logging.CRITICAL, message, status, function, variable, value)
