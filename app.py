from flask import Flask, jsonify, request
from compiler.parser import runParserWithFile
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
    
    fileName = 'code.txt'
    f = open(fileName, 'w')
    f.write(request.data)
    f.close()
    #codeResult = runParserWithFile(fileName)
    codeResult = ''
    print('codeResult', codeResult)
    return codeResult, 200
    #return jsonify({ 'result': result }), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
