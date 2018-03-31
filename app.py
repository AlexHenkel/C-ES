from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print('hello_world')
    return 'Lenguaje C-ES'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
