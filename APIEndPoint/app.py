# -*- coding: utf-8 -*-
#!/usr/bin/python
import flask
from flask import request,jsonify,make_response,abort
import numpy as np
import pandas as pd
app = flask.Flask(__name__)
SERVER_HOST='localhost'
SERVER_PORT=8001

# making data frame from csv file  
data = pd.read_csv("data/customers.csv") 
  
# replacing blank spaces with '_'  
data.columns =[column.replace(" ", "_") for column in data.columns] 

#take filter parameters from URL
#e.g. http://127.0.0.1:5000/params/Name=='John'&Credit_Limit>4000
@app.route('/params/<keyval>')
def params(keyval):
	result = data.query(keyval).to_json()
	print ("Result=>"+ result)
	return result,200,{'Content-Type':'application/json; charset=utf-8'}

@app.errorhandler(404)
def not_found(error):
 	return make_response(jsonify({'Error':'No data found'}),404)

if __name__ == "__main__":
    app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)