# -*- coding: utf-8 -*-
#!/usr/bin/python
import flask
from flask import request,jsonify,make_response
from os import listdir
from os.path import isfile,join,splitext

import pandas as pd
app = flask.Flask(__name__)
SERVER_HOST='localhost'
SERVER_PORT=8001
DATA_SOURCE ='./data/'

#list of data sources
dataDict = {}
datafiles = [f for f in listdir(DATA_SOURCE) if isfile(join(DATA_SOURCE, f))]

#read data sources
for f in datafiles:
	print("=============== Reading Data from source: " + f)
	# reading data frame from csv file
	dataDict[splitext(f)[0]] = pd.read_csv(DATA_SOURCE+f, sep=',')

#read url parameters from URL
#e.g. http://127.0.0.1:8001/getData?query=Name=='John'%26Credit_Limit>4000&source=customer

@app.route('/getData', methods=['GET'])
def getData():
	qstring=request.args.get('query')
	dataSource=request.args.get('source')

	if dataSource in dataDict.keys():
		data = dataDict.get(dataSource)
		result = data.query(qstring).to_json()
	else:
		result = jsonify({'Error':'No such source'})
	return result,200,{'Content-Type':'application/json; charset=utf-8'}

@app.errorhandler(404)
def not_found(error):
 	return make_response(jsonify({'Error':'No data found'}),404)

if __name__ == "__main__":
    app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)