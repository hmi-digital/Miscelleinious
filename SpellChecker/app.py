# -*- coding: utf-8 -*-
#!/usr/bin/python
import flask
from flask import request,jsonify,make_response
from module import spellChecker

app = flask.Flask(__name__)
SERVER_HOST='localhost'
SERVER_PORT=8001

spellChecker.init()

#read url parameters from URL
#e.g. http://127.0.0.1:8001/spellCheck?utterance=I am good

@app.route('/spellCheck', methods=['GET'])
def spellCheck():
	utterance=request.args.get('utterance')

	if utterance is not None:
		result = jsonify({'Utterance':spellChecker.spellCorrect(utterance)})
	else:
		result = jsonify({'Error':'Not able to process'})
	return result,200,{'Content-Type':'application/json; charset=utf-8'}

@app.errorhandler(404)
def not_found(error):
 	return make_response(jsonify({'Error':'Not able to process'}),404)

if __name__ == "__main__":
    app.run(debug=False,host=SERVER_HOST,port=SERVER_PORT,threaded=True)