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


for f in documents:
    filetype = magic.from_file(f, mime=True)
    filedata = None
    if filetype==filetypes[0]:
        filedata = docs_to_text.extract_text_from_pdf(f)
    elif filetype==filetypes[1]:
        filedata = docs_to_text.extract_text_from_txt(f)
    elif filetype==filetypes[2]:
        filedata = docs_to_text.extract_text_from_csv(f)
    elif filetype==filetypes[3]:
        filedata = docs_to_text.extract_text_from_document(f)
    elif filetype==filetypes[4]:
        filedata = docs_to_text.extract_text_from_docx(f)
    elif filetype==filetypes[5]:
        filedata = docs_to_text.extract_text_from_pptx(f)
    
    


