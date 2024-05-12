from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# non-streaming
resp = OpenAI(model='gpt-3.5-turbo').complete("Paul Graham is ")
print(resp)

