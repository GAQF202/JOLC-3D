from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from subprocess import check_call
from Analyzer.gramatica import parser
from Analyzer.gramatica import set_input
#from Instructions.Print import output

import pydot
app= Flask(__name__)
@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"
graphs = []
@app.route('/correr', methods=['POST'])
@cross_origin(supports_credentials=True)
def correr():
    input = {
        'datos' : request.json['prueba']
    }
    #PARSER DE ANALISIS
    set_input(input['datos'])
    parser.parse(input['datos'])
    return "hola"
    #return jsonify({'output':output.getOutput()})

