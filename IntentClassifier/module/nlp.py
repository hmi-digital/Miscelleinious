# -*- coding: utf-8 -*-
import os
import datetime
import codecs
import time
import pickle
import spacy
import numpy as np
import warnings
import configparser
from keras.models import load_model
warnings.filterwarnings("ignore")
scriptDir=os.path.dirname(__file__)
config=configparser.RawConfigParser()
config.read(os.path.join(scriptDir,'..','config','classifier.properties'))
thresholdScore=config.get('Classifier','Classifier.thresholdScore')
logFile=os.path.join(scriptDir,'..','log',str(datetime.datetime.today().strftime('%b'))+'_training.txt')
def logTraining(logDetails):
 if os.path.isfile(logFile):
  dFile=time.strftime("%m/%d/%Y",time.localtime(os.path.getmtime(logFile)))
  dCurrent=datetime.datetime.today().strftime('%m/%d/%Y')
  dateFile=datetime.datetime.strptime(dFile,'%m/%d/%Y')
  dateCurrent=datetime.datetime.strptime(dCurrent,'%m/%d/%Y')
  diff=(dateCurrent-dateFile).days
  if(diff>31):
   f1=codecs.open(logFile,'w','utf-8')
   f1.write(str(datetime.datetime.now(datetime.timezone.utc).astimezone())+" "+logDetails+"\n")
   f1.close()
  else:
   f1=codecs.open(logFile,'a','utf-8')
   f1.write(str(datetime.datetime.now(datetime.timezone.utc).astimezone())+" "+logDetails+"\n")
   f1.close()
 else:
  f1=codecs.open(logFile,'w','utf-8')
  f1.write(str(datetime.datetime.now(datetime.timezone.utc).astimezone())+" "+logDetails+"\n")
  f1.close()
class FakeEmbedder(object):
 def __init__(self,maxLength=100):
  self.maxLength=maxLength
 def embed(self,text):
  return np.random.random((self.maxLength,300))
class Embedder(object):
 def __init__(self,maxLength=100):
  self.maxLength=maxLength
  print("Loading english trained model...")
  self.nlp=spacy.load('en')
  print("...done")
 def embed(self,text):
  return self._pad(self._vectors(text))
 def shape(self):
  return(self.maxLength,300)
 def _vectors(self,text):
  doc=self.nlp(text)
  vectors=[]
  for token in doc:
   vectors.append(token.vector)
  return vectors
 def _pad(self,vectors):
  vectorDim=len(vectors[0])
  sequence=np.zeros((self.maxLength,vectorDim))
  for i,vector in enumerate(vectors):
   if i==self.maxLength:
    break
   sequence[i]=vector
  return sequence
class Predictor(object):
 def __init__(self,embedder,modelPath,intentNamesPath):
  self.model=load_model(modelPath)
  self.intent_names=pickle.load(open(intentNamesPath,"rb"))
  self.embedder=embedder
 def predict(self,text):
  proba=self._predict_proba(text)
  score=proba[0,np.argmax(proba)]
  if(score>=float(thresholdScore)):
   intent=self.intent_names[np.argmax(proba)]
  else:
   intent="NA"
   logTraining("Utterance: "+text+", Probability: "+str(format(score,'.2f'))+", Identified as:"+''.join(self.intent_names[np.argmax(proba)]))
  print("intent",intent)
  print("utterance",text)
  print("score:",proba[0,np.argmax(proba)])
  return intent,score
 def _predict_proba(self,text):
  embedding=self.embedder.embed(text)
  return self.model.predict(np.array([embedding]))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
