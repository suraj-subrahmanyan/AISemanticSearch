import json

from elasticsearch import Elasticsearch #downgraded version 8.11.0 to match server

client = Elasticsearch("http://localhost:9200")

with open('mapping.json', 'r') as reader:
    mappings = json.load(reader)

client.indices.create(index = "sparse_index", mappings = mappings)
print("Inverted index has been created")