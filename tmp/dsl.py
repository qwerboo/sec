curl -XGET 'localhost:9200/_cat/indices?v&pretty'
curl -XGET 'localhost:9200/zcb_rawdata/rawdata/122153?pretty'
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
curl -XGET 'localhost:9200/zcb_rawdata/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "sort": [
    { "timestamp": {"order":"desc"} }
  ],
  "size": 1,
  "_source": [""]
}
'
curl -XPOST 'localhost:9200/_bulk?pretty' -H 'Content-Type: application/json' -d'
{ "index" : { "_index" : "test", "_type" : "type1", "_id" : "1" } }
{ "field1" : "value1" }
{ "delete" : { "_index" : "test", "_type" : "type1", "_id" : "2" } }
{ "create" : { "_index" : "test", "_type" : "type1", "_id" : "3" } }
{ "field1" : "value3" }
{ "update" : {"_id" : "1", "_type" : "type1", "_index" : "test"} }
{ "doc" : {"field2" : "value2"} }
'
