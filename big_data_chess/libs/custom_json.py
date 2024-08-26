from pythonjsonlogger import jsonlogger
import logging

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        # You can customize the format here
        super(CustomJsonFormatter, self).__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['status'] = getattr(record, 'status', None)
        log_record['operation'] = getattr(record, 'operation', None)
        log_record['value'] = getattr(record, 'value', None)
