curl -XGET 'localhost:9200/_cat/indices?v&pretty'
curl -XGET 'localhost:9200/zcb_rawdata/_search?q=*&sort=account_number:asc&pretty&pretty'
curl -XGET 'localhost:9200/zcb_rawdata/_search?q=*&sort=account_number:asc&pretty&pretty'
curl -XGET 'localhost:9200/zcb_rawdata/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "sort": [
    { "_id": "desc" }
  ],
  "size": 1,
  "_source": [""]
}
'
