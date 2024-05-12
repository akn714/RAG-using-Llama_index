import os
import re
import math
import random
import openai
from openai import OpenAI
import pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from dotenv import load_dotenv
load_dotenv()



# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
# MODEL = "text-embedding-ada-002"
MODEL = "text-embedding-3-small"

# Initialize Pinecone
print('[+] initializing pinecone')
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
# pc = Pinecone(api_key='2e33ff86-f1b0-4782-a7b4-dcf6cb6dc34b')

# Define the index name
index_name = os.getenv('INDEX_NAME')

# Create the index if it doesn't exist
if index_name not in pc.list_indexes().names():
    print(f'[+] creating index {index_name}')
    pc.create_index(
        name=index_name,
        dimension=8,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    )

# Instantiate the index
index = pc.Index(index_name)

# Define a function to preprocess text
def preprocess_text(text):
    # Replace consecutive spaces, newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    return text

def process_pdf(file_path):
    # create a loader
    loader = PyPDFLoader(file_path)
    # load your data
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(data)
    # Convert Document objects into strings
    texts = [str(doc) for doc in documents]
    return texts

def process_csv():
    loader = CSVLoader(file_path='./example_data/mlb_teams_2012.csv')
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(data)
    # Convert Document objects into strings
    texts = [str(doc) for doc in documents]
    return texts



client = OpenAI()

# Define a function to create embeddings
def create_embeddings(texts):
    i = 1
    embeddings_list = []
    for text in texts:
        try:
            res = client.embeddings.create(input = [text], model=MODEL, dimensions=8)
            print('[+] embedding', i, 'created')
            # print('[+] embedding:', res.data[0].embedding)
            # res = openai.Embedding.create(input=[text], engine=MODEL)
            embeddings_list.append(res.data[0].embedding)
        except Exception as e:
            print(f'[-] {i} error in OpenAI().embedding')
        i += 1
    print()
    return embeddings_list

# Define a function to upsert embeddings to Pinecone
def upsert_embeddings_to_pinecone(index, embeddings, ids):
    # vectors = [(id, embedding) for id, embedding in zip(ids, embeddings)]
    # vectors = [(ids[0], embedding) for embedding in embeddings]
    vectors = [{"id":str(random.randint(100000000, 1000000000)), "values":embedding} for embedding in embeddings]
    print('[+] vectors:', vectors)
    index.upsert(vectors=vectors)

# Process a PDF and create embeddings
file_path = "../how-to-win-friends-and-influence-people.pdf"  # Replace with your actual file path

print('[+] processing pdf')
texts = process_pdf(file_path)

print('[+] creating embeddings')
embeddings = create_embeddings(texts)
# print(embeddings)

print('[+] upserting embeddings')
# Upsert the embeddings to Pinecone
upsert_embeddings_to_pinecone(index, embeddings, [file_path])



