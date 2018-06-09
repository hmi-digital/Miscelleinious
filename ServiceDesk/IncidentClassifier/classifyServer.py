# -*- coding: utf-8 -*-
import os
import re
import module as m
import trainModel
import flask
from flask import request,jsonify,make_response,abort
SERVER_HOST='localhost'
SERVER_PORT=8001
scriptDir=os.path.dirname(__file__)
myMdoel=trainModel.incidentModel()
myMdoel.train()
m.initialize()
app=flask.Flask(__name__)
app.config["DEBUG"]=False
@app.route('/classify',methods=['GET'])
def process():
 if not(request.args.get('userUtterance')):
  abort(404)    
 if 'userUtterance' in request.args:
  userUtterance=request.args['userUtterance']
  utter=re.sub(r'[^a-zA-Z ]','',userUtterance)
  combinations=m.genUtterances(utter)
  result=m.processUtterance(combinations)
  return jsonify(result),200,{'Content-Type':'application/json; charset=utf-8'}
 else:
  return jsonify("{'Error': 'No utterance provided. Please provide the same'}"),200,{'Content-Type':'application/json; charset=utf-8'}
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'Error':'Please use correct url and its parameter'}),404)
if __name__=='__main__':
 app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
