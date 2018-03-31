from flask import Flask, jsonify, request
from compiler.parser import runParser
import parser

app = Flask(__name__)

@app.route('/')
def hello_world(): 
    return 'Lenguaje C-ES'

@app.route('/execute', methods=['POST'])
def executeCode():
    if not request.json:
        return jsonify({ 'error': 'No json data sent.' }), 400
    
    if not 'code' in request.json:
        return jsonify({ 'error': 'No \'code\' property provided.' }), 400

    code = request.json['code']
    result = runParser()
    print('code received:', code)
    return jsonify({ 'result': result }), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
