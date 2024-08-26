curl -X GET "localhost:9200/log_big_data_chess/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2024-08-26T00:00:00Z",
        "lte": "2024-08-26T13:00:00Z"
      }
    }
  }
}
'
