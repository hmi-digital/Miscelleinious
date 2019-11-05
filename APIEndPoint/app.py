# -*- coding: utf-8 -*-
#!/usr/bin/python
import flask
from flask import request,jsonify,make_response
from os import listdir
from os.path import isfile,join,splitext
import pandas as pd
from module import dataUtil

app = flask.Flask(__name__)
SERVER_HOST='localhost'
SERVER_PORT=8001

dataUtil.readData()

#read url parameters from URL
#e.g. http://127.0.0.1:8001/getData?query=Name=='John'%26Credit_Limit>4000&source=customer

@app.route('/getData', methods=['GET'])
def getData():
	qstring=request.args.get('query')
	dataSource=request.args.get('source')

	if dataSource in dataUtil.dataDict.keys():
		data = dataUtil.dataDict.get(dataSource)
		result = data.query(qstring).to_json(orient='index')
	else:
		result = jsonify({'Error':'No such source'})
	return result,200,{'Content-Type':'application/json; charset=utf-8'}

@app.errorhandler(404)
def not_found(error):
 	return make_response(jsonify({'Error':'No data found'}),404)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == "__main__":
    app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)