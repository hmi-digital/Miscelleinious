# -*- coding: utf-8 -*-
import os
import re
import module as m
import trainModel
import flask
from flask import request,jsonify
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
 if 'userUtterance' in request.args:
  userUtterance=request.args['userUtterance']
  utter=re.sub(r'[^a-zA-Z ]','',userUtterance)
  combinations=m.genUtterances(utter)
  Result=m.processUtterance(combinations)
  return jsonify(Result)
 else:
  return jsonify("{'Error': 'No utterance provided. Please provide the same'}")
if __name__=='__main__':
 app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
