from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

def save_docs():
    # saving all files in /docs folder
    return

def load_docs():
    # loading all files in /docs using SimpleDirectoryReader
    debug('loading doc')
    documents = SimpleDirectoryReader('docs').load_data()
    return documents

def create_index(documents):
    # creating index using VectorStoreIndex and returning that index
    debug('making index')
    index = VectorStoreIndex.from_documents(documents)
    return index

def create_query_engine(index):
    # crating query engine using index.as_query_engine()
    debug('generating query engine')
    query_engine = index.as_query_engine()
    return query_engine

def generate_response(query_engine, query):
    # generate response for one query using query engine
    debug('generating response')
    response = query_engine.query(query)
    # debug('response:', response)
    return response

def debug(x):
    print('[+]', x)





