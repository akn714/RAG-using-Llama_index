import os
from dotenv import load_dotenv
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

print('loading doc')
documents = SimpleDirectoryReader('docs').load_data()
print('making index')
index = VectorStoreIndex.from_documents(documents)

print('generating query engine')
query_engine = index.as_query_engine()

print('generating response')
response = query_engine.query('what is this book about')
print('response:', response)



