from elasticsearch import Elasticsearch
from config import hostName, nameIndex
import jsonlines

#retrieve results and evaluate

client = Elasticsearch(hostName)

def queryFun(query):
    results = client.search(index=nameIndex, body={"query": {"multi_match": {"query": query, "fields": ["title", "summary"]}}})
    for hits in results['hits']['hits']:
        score = hits['_score']

        #find the original text and summary for each relevant doc's id
        id = hits['_id']
        with jsonlines.open('processed_papers_final.jsonl', 'r') as reader:
            for lines in reader:
                if (id == lines['id']):
                    print(lines['title'])
                    print(lines['summary'])

        print(f"Score: {score}\n") #evaluate relatively

if __name__ == '__main__':
    print("Query #1\n")
    queryFun("Gramatical Relationships (GRs)")
    print("Query #2\n")
    queryFun("Occam's Razor")
    
    
    # structure of results
    # print (results['hits'])











