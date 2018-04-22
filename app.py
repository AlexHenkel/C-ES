from flask import Flask, jsonify, request, render_template, url_for
from flask_cors import CORS, cross_origin
from compiler.parser import runParserWithFile
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def ui(): 
    return render_template('index.html')
   
@app.route('/manual')
def manual(): 
    return render_template('manual.html')

@app.route('/inicio')
def inicio(): 
    return render_template('inicio.html')

@app.route('/variables')
def variables(): 
    return render_template('variables.html')

@app.route('/funciones')
def funciones(): 
    return render_template('funciones.html')

@app.route('/operadores')
def operadores(): 
    return render_template('operadores.html')

@app.route('/control-de-flujo')
def control_de_flujo(): 
    return render_template('control_de_flujo.html')

@app.route('/bloque-principal')
def bloque_principal(): 
    return render_template('bloque_principal.html')

@app.route('/ejemplos')
def ejemplos(): 
    return render_template('ejemplos.html')

@app.route('/execute', methods=['POST'])
@cross_origin()
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
    codeResult = runParserWithFile(fileName)
    #codeResult = ''
    print('codeResult', codeResult)
    return codeResult, 200
    #return jsonify({ 'result': result }), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
