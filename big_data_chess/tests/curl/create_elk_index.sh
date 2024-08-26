curl -X PUT "localhost:9200/log_big_data_chess" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "message": {
        "type": "text"
      },
      "timestamp": {
        "type": "date",
        "format": "strict_date_time"
      },
      "level": {
        "type": "keyword"
      },
      "logger_name": {
        "type": "keyword"
      },
      "status": {
        "type": "keyword"
      },
      "function": {
        "type": "keyword"
      },
      "variable": {
        "type": "keyword"
      },
      "value": {
        "type": "keyword"
      }
    }
  }
}
'
