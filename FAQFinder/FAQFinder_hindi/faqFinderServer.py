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
myMdoel=trainModel.faqModel()
myMdoel.train()
m.initialize()
app=flask.Flask(__name__)
app.config["DEBUG"]=False
@app.route('/faq',methods=['GET'])
def process():
 if not(request.args.get('userUtterance')):
  abort(404)
 userUtterance=request.args['userUtterance']
 utter= userUtterance
 combinations=m.genUtterances(utter)
 result=m.processUtterance(combinations)
 if result:
  result=m.processResult(result)
  return result,200,{'Content-Type':'application/json; charset=utf-8'}
 else:
  m.logTraining(utter)
  result=jsonify({'response':'NA','info':'NA'})
  return result,200,{'Content-Type':'application/json; charset=utf-8'}
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'Error':'Please enter a query'}),404)
def main():
 m.initialize()
 utterance="भीम क्या है और इसका प्रयोग क्यों करना चाहिए ?"
 combinations=m.genUtterances(utterance)
 print(combinations)
 result=m.processUtterance(combinations)
 print(result)
 m.processResult(result)
if __name__=='__main__':
 app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
