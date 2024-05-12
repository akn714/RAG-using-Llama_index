import os
from dotenv import load_dotenv
import pinecone
from llama_index import LlamaIndex
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

load_dotenv()

def connect_to_pinecone(api_key, index_name):
    pinecone.init(api_key=api_key)
    index = pinecone.Index(index_name)
    return index

def create_llama_index(documents):
    llama_index = LlamaIndex()
    llama_index.build_index(documents)
    return llama_index

def retrieve_documents(llama_index, query, k=5):
    retrieved_doc_ids = llama_index.search(query, k=k)c
    return retrieved_doc_ids

def generate_responses(retrieved_docs, queries):
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
    retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index_path=None)
    generator = RagSequenceForGeneration.from_pretrained("facebook/rag-token-base", retriever=retriever)

    responses = []
    for query, doc_ids in zip(queries, retrieved_docs):
        documents = [retrieve_document_from_pinecone(doc_id) for doc_id in doc_ids]
        inputs = tokenizer(query, documents, return_tensors="pt", padding=True)
        outputs = generator.generate(input_ids=inputs["input_ids"])
        responses.append(tokenizer.decode(outputs[0], skip_special_tokens=True))
    
    return responses

def retrieve_document_from_pinecone(doc_id):
    # Retrieve document from Pinecone database based on doc_id
    pass

def main():
    # Connect to Pinecone
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_index_name = os.getenv('INDEX_NAME')
    pinecone_index = connect_to_pinecone(pinecone_api_key, pinecone_index_name)

    # Prepare documents and queries
    documents = ['how-to-win-friends-and-influence-people.pdf']  # List of documents
    queries = ['what this book is actually about?', 'who is the author of this book?']    # List of queries

    # Create Llama index
    llama_index = create_llama_index(documents)

    # Retrieve relevant documents
    retrieved_docs = []
    for query in queries:
        retrieved_docs.append(retrieve_documents(llama_index, query))

    # Generate responses
    responses = generate_responses(retrieved_docs, queries)

    # Print or return responses
    for query, response in zip(queries, responses):
        print(f"Query: {query}")
        print(f"Response: {response}")
        print("=" * 50)

if __name__ == "__main__":
    main()
