from elasticsearch import Elasticsearch
from config import hostName, nameIndex
import jsonlines

#retrieve results and evaluate

client = Elasticsearch(hostName)

def queryFun(query):
    # results = client.search(index=nameIndex, body={"query": {"multi_match": {"query": query, "fields": ["title", "summary"]}}}) <-- simple
    query = client.search(index=nameIndex, body= {"query": {"bool" : {"should" : [{"multi_match" : {"query" : query, "fuzziness": "AUTO", "fields": ["title", "summary"]}}], "minimum_should_match": 1}}})
     
    for hits in query['hits']['hits']:
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
    userInput = input()
    queryFun(userInput)


    # calculate Precision@N for each query
    # print("Query #1\n") #2/3 (0.66)
    # queryFun("Gramatical Relationships (GRs)") 
    # print("Query #2\n") #2/2 (1)
    # queryFun("Occam's Razor")
    # print("Query #3\n")
    # queryFun("Imapct of machien learning on traffic lights") #purposeful typo
    # print("Query #4\n")
    # # queryFun("transformer architecture")
    # print("Query #5\n")
    # queryFun("Exploring decision tree forest")
    # print("Query #6\n")
    # queryFun("Security via face verification and fingerprinting systems")
    # print("Query #7\n")
    # queryFun("Give me papers on sankrit")

    # bad with multiple ideas + typos; good with keyword searches (expected)


    # formulas
    # Precision@N (Recall is tedious) 
    
    # structure of results
    # print (results['hits'])











