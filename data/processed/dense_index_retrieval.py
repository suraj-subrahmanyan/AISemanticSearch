import jsonlines
from transformers import AutoModel, AutoTokenizer
import chromadb
import torch

if (torch.cuda.is_available()):
    device_type = 'cuda'
else:
    device_type = 'cpu'

device = torch.device(device_type)

tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-base-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-base-en-v1.5')

model.to(device)

chroma_client = chromadb.PersistentClient(path="./dense_chroma_db")

dense_index = chroma_client.get_or_create_collection(name="dense_index")

def Metadata_id_doc_embeddings():
    with jsonlines.open('processed_papers_final.jsonl', 'r') as reader1, jsonlines.open('dense_text.jsonl', 'r') as reader2:
        id_list = []
        metadata_list = []
        documents_list = []
        embeddings_list = []

        for lines1, lines2 in zip(reader1, reader2):
            #metadata
            metadata_dict = {}
            s_id = lines1['id']
            s_split_id = s_id.split('/')
            metadata_dict['arxiv_id'] = s_split_id[-1]
            s_pub = lines1['published']
            metadata_dict['published_date'] = s_pub[0:10]
            metadata_dict['title'] = lines1['title']
            metadata_dict['category'] = lines1['category']
            metadata_dict['link'] = lines1['link']
        
            #ids
            id_list.append(s_split_id[-1])
            metadata_list.append(metadata_dict)

            #doc (title+summary)
            documents_list.append(lines2['title'] + " " + lines2['summary'])

            #embeddings
            text_to_embed = lines2['title'] + " " + lines2['summary']
            encoded_text = tokenizer(text_to_embed, return_tensors = 'pt', truncation=False)
            gpu_encoded_text = {}

            for key, val in encoded_text.items():
                gpu_encoded_text[key] = val.to(device)
            
            encoded_text = gpu_encoded_text

            with torch.no_grad():  
                output = model(**encoded_text)

            embeddings = output.pooler_output[0].tolist()
            embeddings_list.append(embeddings)

    return id_list, documents_list, embeddings_list, metadata_list

def addCollection():
    Ids, Documents, Embeddings, Metadatas = Metadata_id_doc_embeddings()

    dense_index.add(
        ids = Ids,
        embeddings = Embeddings,
        documents = Documents,
        metadatas = Metadatas,
    )

def make_bge_query(query_list):
    bge_queries = []
    for queries in query_list:
        bge_queries.append(f"For query: {queries}")
    
    return bge_queries

if __name__ == '__main__':
    # addCollection()

    query_text = ["Find papers related to sanskrit"]
    query_text = make_bge_query(query_text)
    encoded_query = tokenizer(query_text, return_tensors = 'pt', truncation=False)
    gpu_encoded_query = {}

    for key, val in encoded_query.items():
        gpu_encoded_query[key] = val.to(device)
    
    encoded_query = gpu_encoded_query

    with torch.no_grad():
        query_output = model(**encoded_query)

    query_embedding = query_output.pooler_output[0].tolist() 

    results = dense_index.query(
        query_embeddings = [query_embedding],
        n_results = 5
    )

    print(results)