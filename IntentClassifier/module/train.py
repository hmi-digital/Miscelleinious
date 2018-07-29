# -*- coding: utf-8 -*-
import json
import numpy as np
import pickle
import warnings
from keras.layers import Dense,Input,Flatten
from keras.layers import Conv1D,MaxPooling1D
from keras.models import Model,load_model
from.nlp import Embedder
embedder=Embedder()
warnings.filterwarnings("ignore")
class intentModel:
 def __init__(self):
  print("WARNING - Training intent model...")
 def train(self):
  def loadData(dataDir,limit=0):
   examples=[]
   intentNames={}
   with open(dataDir+'/intents.json')as dataFile:
    data=json.load(dataFile)
   for i,intent in enumerate(data):
    intentNames[i]=intent["name"]
    for message in intent["utterances"]:
     examples.append((message,i))
   np.random.shuffle(examples)
   if limit>=1:
    examples=examples[:limit]
   messages,intents=zip(*examples)
   return examples,intentNames
  def dummyEncode(array,numClasses=None):
   array=np.array(array)
   if numClasses is None:
    numClasses=max(array)+1
   result=np.zeros((len(array),numClasses))
   result[np.arange(len(array)),array]=1
   return result
  def createDataset(type):
   if type=='train':
    dataDir='data/train'
   elif type=='test':
    dataDir='data/test'
   else:
    assert(False),"Type must be train or dev"
   examples,intentNames=loadData(dataDir)
   X=[]
   y=[]
   for example in examples:
    message,intent=example[0],example[1]
    X.append(embedder.embed(message))
    y.append(intent)
   return np.array(X),dummyEncode(np.array(y)),intentNames
  X_train,y_train,intentNamesTrain=createDataset('train')
  X_test,y_test,intentNamesTest=createDataset('test')
  X,y,intentNames=X_train,y_train,intentNamesTrain
  def buildModel(inputShape):
   sequences=Input(shape=inputShape)
   x=Conv1D(16,5,activation='relu')(sequences)
   x=MaxPooling1D(2)(x)
   x=Conv1D(16,3,activation='relu')(x)
   x=MaxPooling1D(2)(x)
   x=Flatten()(x)
   x=Dense(16,activation='relu')(x)
   preds=Dense(len(intentNames),activation='softmax')(x)
   model=Model(input=sequences,output=preds)
   model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])
   return model
  model=buildModel((X.shape[1],X.shape[2]))
  history=model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=20,batch_size=128)
  def saveModel(model):
   model.save('model/cnnModel')
  saveModel(model)
  pickle.dump(intentNames,open("model/intentNames.m","wb"))
  loadedModel=load_model('model/cnnModel')
  loadedIntentNames=pickle.load(open("model/intentNames.m","rb"))
  def predict(model,text):
   embedding=embedder.embed(text)
   return model.predict(np.array([embedding]))
  def translate(prediction,intentNames):
   return intentNames[np.argmax(prediction)]
  def suggest(text):
   prediction=predict(loadedModel,text)
   return translate(prediction,loadedIntentNames)
def main():
 myModel=intentModel()
 myModel.train()
if __name__=="__main__":
 main()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
