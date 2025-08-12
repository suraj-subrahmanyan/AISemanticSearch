import requests
import time

# make sure to manage rate limits

def apiCall(base_url, endpoints_file):
    wait_time = 3
    for endpoints, file_name in endpoints_file:
        r = requests.get(base_url + endpoints)

        if (r.status_code == 200):
            with open(file_name, 'w') as w:
                w.write(r.text)
            print("Sucessful")
        else:
            print(f"There was an error for {file_name}")

        time.sleep(wait_time)

if __name__ == "__main__":
    base_url = "http://export.arxiv.org/api/query?"

    endpoints_file = [("search_query=cat:cs.AI&start=0&max_results=1000", 'AI_papers.xml'),#1000, fair play
                 ("search_query=cat:cs.LG&start=0&max_results=1000", 'LG_papers.xml'), #i.e, machine learning
                 ("search_query=cat:cs.CL&start=0&max_results=1000", 'CL_papers.xml'),
                 ("search_query=cat:cs.CV&start=0&max_results=1000", 'CV_papers.xml'),
                 ("search_query=cat:cs.IR&start=0&max_results=1000", 'IR_papers.xml')]
    
    apiCall(base_url, endpoints_file)

