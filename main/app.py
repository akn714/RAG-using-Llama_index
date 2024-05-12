import os
from dotenv import load_dotenv
from flask import *
import main_main as utils
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    queries = request.form.getlist('strings[]')

    print(files[0])
    for file in files:
        file.save(os.path.join('docs', file.filename))
    
    print(queries)

    return "uploaded"

@app.route('/api', methods=['POST'])
def api():
    files = request.files.getlist('file')
    queries = [request.form.get('query')]

    for file in files:
        file.save(os.path.join('docs', file.filename))

    # for file in files:
    #     utils.save_docs(file)

    docs = utils.load_docs()

    index = utils.create_index(docs)

    query_engine = utils.create_query_engine(index)

    responses = []

    for q in queries:
        res = utils.generate_response(query_engine, q)
        responses.append(res)
    
    for file in files:
        filepath = os.path.join('docs', file.filename)
        os.remove(filepath)
    
    return str(responses[0])


if __name__ == '__main__':
    app.run(debug=True)




