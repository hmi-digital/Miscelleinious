# -*- coding: utf-8 -*-
import os
import configparser
import re
import codecs
import _pickle as cPickle
import datetime
import glob
import time
from flask import jsonify
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import linear_kernel
scriptDir=os.path.dirname(__file__)
config=configparser.RawConfigParser()
config.read(os.path.join(scriptDir,'..','config','classifier.properties'))
thresholdScore=config.get('Classifier','Classifier.thresholdScore')
logFile=os.path.join(scriptDir,'..','log',str(datetime.datetime.today().strftime('%b'))+'_training.txt')
synonymFile=os.path.join(scriptDir,'..','data','dictionary','synonyms_en.txt')
with codecs.open(synonymFile,'r','utf-8')as rawSynonymsFileobj:
 rawSynonyms=rawSynonymsFileobj.read()
 rawSynonyms=rawSynonyms.split('\n')
synonymsList=[]
for i in rawSynonyms:
 synonymsList.append(i.split(','))
def initialize():
 global picklePath
 global classes
 global utterance
 global tfidfVec
 global svd
 global trainLSA
 global stopwordList
 picklePath=os.path.join(scriptDir,'..','model')
 classes=cPickle.load(open(os.path.join(picklePath,'classes.m'),'rb'))
 utterance=cPickle.load(open(os.path.join(picklePath,'utterance.m'),'rb'))
 tfidfVec=cPickle.load(open(os.path.join(picklePath,'tfidfVec.m'),'rb'))
 svd=cPickle.load(open(os.path.join(picklePath,'svd.m'),'rb'))
 trainLSA=cPickle.load(open(os.path.join(picklePath,'trainLSA.m'),'rb'))
 stopwordFile=os.path.join(scriptDir,'..','data','dictionary','stopwords_en.txt')
 arrayWords=[]
 stopWords=[]
 sList=[line.rstrip('\n')for line in codecs.open((stopwordFile),'r+','utf-8')]
 for line in sList:
  if line!="":
   arrayWords.append(line.split(','))
 for a_word in arrayWords:
  for s_word in a_word:
   if(re.sub(' ','',s_word))!="":
    stopWords.append(s_word)
 swList=set(stopWords)
 stopwordList=set(stopwords.words('english'))|swList
def stopwordRemover(utterance):
 word_tokens=word_tokenize(utterance)
 return ' '.join([w for w in word_tokens if not w in stopwordList])
def replace_nth(string,sub,repl,nth):
 find=string.find(sub)
 i=find!=-1
 while find!=-1 and i!=nth:
  find=string.find(sub,find+1)
  i+=1
 if i==nth:
  return string[:find]+repl+string[find+len(sub):]
 return string
def wordReplacer(utter,matchedDict,combinations):
 matchedDict=matchedDict.copy()
 while(len(matchedDict)>0):
  replacement=matchedDict.popitem()
  for wordReplacement in replacement[1]['synonym']:
   new_utter=utter.replace(replacement[0],wordReplacement)
   combinations.append(new_utter)
   wordReplacer(new_utter,matchedDict,combinations)
def genSentences(utter,matchedDict,combinations):
 matchedDict=matchedDict.copy()
 while(len(matchedDict)>0):
  replacement=matchedDict.popitem()
  for count in range(replacement[1]['count']):
   for wordReplacement in replacement[1]['synonym']:
    new_utter=replace_nth(utter,replacement[0],wordReplacement,count+1)
    combinations.append(new_utter)
    wordReplacer(new_utter,matchedDict,combinations)
def processUtterance(utter):
 scoreList={}
 idList={}
 for inputQuery in utter:      
  query=stopwordRemover(inputQuery.lower())
  query=[query]
  test=tfidfVec.transform(query).toarray()
  LSATest=svd.transform(test)
  cosineSimilarities=linear_kernel(LSATest,trainLSA).flatten()
  related_docs_indices=cosineSimilarities.argsort()[::-1]
  for i in range(len(related_docs_indices)):
   fID=related_docs_indices[i]
   fScore=cosineSimilarities[fID]
   fClasses=classes[related_docs_indices[i]]
   if(fClasses in scoreList):
    scoreList[fClasses]=max(fScore,scoreList[fClasses])
    if(fScore>cosineSimilarities[idList.get(fClasses)]):
     idList[fClasses]=fID
   else:
    scoreList[fClasses]=fScore
    idList[fClasses]=fID
 orderedClasses=sorted(scoreList,key=scoreList.get,reverse=True)
 print('\tResult- class: '+orderedClasses[0]+' score:'+"{:.2f}".format(scoreList[orderedClasses[0]]))
 if(float(scoreList[orderedClasses[0]])>=float(thresholdScore)):
  response={'class':orderedClasses[0],'score':"{:.2f}".format(scoreList[orderedClasses[0]])}
 else:
  response={'class':'NA','score':"{:.2f}".format(scoreList[orderedClasses[0]])}
  logTraining("Original: "+inputQuery+" Processed:"+''.join(query))
 return response
def genUtterances(utter):
 matched={}
 utteranceSet=set(utter.split())
 for synonym in synonymsList:
  for word in set(synonym)&utteranceSet:
   count=utter.split().count(word)
   matched[word]={'synonym':list(set(synonym)-set([word])),'count':count}
 combinations=[utter]
 genSentences(utter,matched,combinations)
 combinations.sort()
 return combinations
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
# Created by pyminifier (https://github.com/liftoff/pyminifier)
