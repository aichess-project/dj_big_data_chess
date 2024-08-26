curl -X PUT "http://localhost:9200/log_big_data_chess" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      },
      "message": {
        "type": "text"
      },
      "loglevel": {
        "type": "keyword"
      },
      "status": {
        "type": "keyword"
      },
      "operation": {
        "type": "keyword"
      },
      "value": {
        "type": "integer"
      }
    }
  }
}'
