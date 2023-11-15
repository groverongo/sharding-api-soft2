from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://172.22.139.146:30000/')
db = client['clima']
collection = db['clima']

# get method and query parameters
@app.get('/')
def get_clima():
    temperatura = round(float(request.args.get('temperatura')))
    fecha = request.args.get('fecha')
    # build the query
    query = {}
    query['fecha'] = fecha
    query['$or'] = [
        {'temperatura_minima': {'$gte': temperatura, '$lt': temperatura + 1}},
        {'temperatura_maxima': {'$gte': temperatura, '$lt': temperatura + 1}},
    ]

    print(query)

    # execute the query
    cursor = collection.find(query)
    # build the result
    result = []
    for document in cursor:
        document.pop('_id')
        result.append(document)

    # return the result
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)