from flask import Flask, jsonify, request
from compiler.parser import runParser
import json

app = Flask(__name__)

@app.route('/')
def hello_world(): 
    return 'Lenguaje C-ES'

@app.route('/execute', methods=['POST'])
def executeCode():

    try:
        header = request.headers['Content-Type']
    except Exception as error:
        return jsonify({ 'error': 'No headers sent.' }), 400

    if not header == 'text/plain':
        return jsonify({ 'error': 'No correct header sent.' }), 400
    
    f = open('code.txt','w')
    f.write(request.data)
    f.close()
    return jsonify({ 'result': request.data }), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
