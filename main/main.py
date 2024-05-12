from dotenv import load_dotenv
import os
import magic
import docs_to_text

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

documents=[]
list_of_queries = []

filetypes = [
    'application/pdf', # pdf
    'text/plain', # txt
    'text/csv', # csv
    'application/msword', # doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', # docx
    # 'application/vnd.ms-powerpoint', # ppt
    'application/vnd.openxmlformats-officedocument.presentationml.presentation' # pptx
]

# for d in documents:

    
    


