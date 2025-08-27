import json
import jsonlines

from config import hostName, nameIndex
from elasticsearch import Elasticsearch #downgraded version 8.11.0 to match server
from elasticsearch import helpers

client = Elasticsearch(hostName)

def createEmptyIndex():
    try:
        with open('mapping.json', 'r') as reader:
            mappings = json.load(reader)

        client.indices.create(index = nameIndex, mappings = mappings)
        print("Inverted index has been created")
    except:
        print("The inverted index has already been created")

def ingestDocuments():
    with jsonlines.open('nlp_text.jsonl', 'r') as reader:
        for lines in reader:
            temp_dict = {}
            temp_dict['title'] = lines['title']
            temp_dict['summary'] = lines['summary']            
            yield{
                "_index": nameIndex,
                "_id": lines['id'],
                "_source": temp_dict
            }

if __name__ == '__main__':
    #createEmptyIndex()

    helpers.bulk(client, ingestDocuments())

    # check document count - 5000 json obj. (docs)
    # response = client.count(index=nameIndex)
    # print(response['count'])


    #test if index present?
    # if client.indices.exists(index=nameIndex):
    #     print("index created")
    # else:
    #     print("index is not present, error")

