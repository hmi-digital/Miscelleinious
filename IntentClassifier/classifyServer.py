# -*- coding: utf-8 -*-
import os
import re
import module as m
import flask
from flask import request,jsonify,make_response,abort
SERVER_HOST='localhost'
SERVER_PORT=8001
scriptDir=os.path.dirname(__file__)
myModel=m.intentModel()
myModel.train()
embedder=m.Embedder()
predictor=m.Predictor(embedder,'model/cnnModel','model/intentNames.m')
app=flask.Flask(__name__)
app.config["DEBUG"]=False
def processUtterance(utter):
 response={}
 intent,score=predictor.predict(utter)
 response["text"]=utter
 response["intent"]=intent
 response["score"]=str(format(score,'.2f'))
 return response
@app.route('/classify',methods=['GET'])
def process():
 if not(request.args.get('userUtterance')):
  abort(404)
 if 'userUtterance' in request.args:
  userUtterance=request.args['userUtterance']
  return jsonify(processUtterance(userUtterance)),200,{'Content-Type':'application/json; charset=utf-8'}
 else:
  return jsonify("{'Error': 'No utterance provided. Please provide the same'}"),200,{'Content-Type':'application/json; charset=utf-8'}
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'Error':'Please use correct url and its parameter'}),404)
if __name__=='__main__':
 app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=False)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
