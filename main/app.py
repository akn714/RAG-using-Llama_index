from flask import *
import main_main as utils

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def main():
    files = request.files.getlist('file')
    queries = []

    for file in files:
        file.save(os.path.join('docs', filename))

    # for file in files:
    #     utils.save_docs(file)

    docs = utils.load_docs()

    index = utils.create_index(docs)

    query_engine = utils.create_query_engine(index)

    responses = []

    for q in queries:
        res = utils.generate_response(q)
        responses.append(res)
    
    return responses






