curl - XGET 'localhost:9200/_cat/indices?v&pretty'
curl - XGET 'localhost:9200/zcb_rawdata/rawdata/122153?pretty'
curl - XGET 'localhost:9200/zcb_rawdata/_search?pretty' - d'
{
    "query": {"match_all": {}},
    "sort": [
        {"_id": "desc"}
    ],
    "size": 1,
    "_source": [""]
}
'
curl - XGET 'localhost:9200/zcb_rawdata/_search?pretty' - d'
{
    "sort": [
        {"timestamp": {"order": "desc"}}
    ],
    "size": 1,
    "_source": [""]
}
'
curl -XGET 'localhost:9200/sec_file/_search?pretty' -H 'Content-Type: application/json' -d'
{
    "query": {"match": {"rawdata": "<tr>"}},
    "_source": [""]
}
'


curl - XPOST 'localhost:9200/_bulk?pretty' - d'
{"index": {"_index": "test", "_type": "type1", "_id": "1"}}
{"field1": "value1"}
{"delete": {"_index": "test", "_type": "type1", "_id": "2"}}
{"create": {"_index": "test", "_type": "type1", "_id": "3"}}
{"field1": "value3"}
{"update": {"_id": "1", "_type": "type1", "_index": "test"}}
{"doc": {"field2": "value2"}}
'

# GET /<logstash-{now/d}>/_search
curl -XGET 'localhost:9200/%3Clogstash-%7Bnow%2Fd%7D%3E/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query" : {
    "match": {
      "test": "data"
    }
  }
}
'

curl -XPUT 'localhost:9200/twitter/tweet/1?pretty' -H 'Content-Type: application/json' -d'
{
    "user" : "kimchy",
    "post_date" : "2009-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
'
curl -XPUT 'localhost:9200/twitter/tweet/1?version=2&pretty' -H 'Content-Type: application/json' -d'
{
    "message" : "elasticsearch now has versioning support, double cool!"
}
'

curl -XPUT 'localhost:9200/twitter/tweet/1?op_type=create&pretty' -H 'Content-Type: application/json' -d'
{
    "user" : "kimchy",
    "post_date" : "2009-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
'
curl -XPOST 'localhost:9200/twitter/tweet/1?routing=kimchy&pretty' -H 'Content-Type: application/json' -d'
{
    "user" : "kimchy",
    "post_date" : "2009-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
'

curl -XPUT 'localhost:9200/twitter/tweet/1?pretty' -H 'Content-Type: application/json' -d'
{
    "counter" : 1,
    "tags" : ["red"]
}
'
curl -XPOST 'localhost:9200/twitter/_delete_by_query?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "message": "some message"
    }
  }
}
'

curl -XPOST 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d'
{
   "query" : {
      "term" : { "product" : "chocolate" }
   },
   "sort" : [
       {
          "offer.price" : {
             "mode" :  "avg",
             "order" : "asc",
             "nested_path" : "offer",
             "nested_filter" : {
                "term" : { "offer.color" : "blue" }
             }
          }
       }
    ]
}
'
