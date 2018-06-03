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
config.read(os.path.join(scriptDir,'..','config','faqFinder.properties'))
thresholdScore=config.get('faqFinder','finder.thresholdScore')
similarityIndexScore=config.get('faqFinder','finder.similarityIndex')
logFile=os.path.join(scriptDir,'..','log',str(datetime.datetime.today().strftime('%b'))+'_training.txt')
corpusItems=len(glob.glob1(os.path.join(scriptDir,'..','data','domain'),'*.txt'))
synonymFile=os.path.join(scriptDir,'..','data','dictionary','synonyms_en.txt')
with codecs.open(synonymFile,'r','utf-8')as rawSynonymsFileobj:
 rawSynonyms=rawSynonymsFileobj.read()
 rawSynonyms=rawSynonyms.split('\n')
synonymsList=[]
for i in rawSynonyms:
 synonymsList.append(i.split(','))
def initialize():
 global picklePath
 global corpus
 global faq
 global tfidfVec
 global svd
 global trainLSA
 global stopwordList
 picklePath=os.path.join(scriptDir,'..','model')
 corpus=cPickle.load(open(os.path.join(picklePath,'corpus.m'),'rb'))
 faq=cPickle.load(open(os.path.join(picklePath,'faq.m'),'rb'))
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
 result={}
 for query in utter:
  query=stopwordRemover(query.lower())
  query=[query]
  test=tfidfVec.transform(query).toarray()
  LSATest=svd.transform(test)
  cosineSimilarities=linear_kernel(LSATest,trainLSA).flatten()
  related_docs_indices=cosineSimilarities.argsort()[:-4:-1]
  for fID in related_docs_indices:
   fScore=cosineSimilarities[fID]
   if(fID in result):
    result[fID]=max(fScore,result[fID])
   else:
    result[fID]=fScore
 noOfTopResults=3
 maxCosineVal=max(result.values())
 result={key:result[key]for key in result if key in sorted(result,key=result.get,reverse=True)[:noOfTopResults]}
 print('Result:',result)
 finalDocIndices={id:{'cosineVal':cosineVal,'sim_diff':maxCosineVal-cosineVal}for(id,cosineVal)in result.items()if(id>=corpusItems)&(cosineVal>float(thresholdScore))&(maxCosineVal-cosineVal<float(similarityIndexScore))}
 return finalDocIndices
def processResult(result):
 bestScoreID=next(iter(result))
 if(result[bestScoreID]['cosineVal']>=float(thresholdScore)):
  q,a=faq[int(bestScoreID)-corpusItems].split('?')
  ans=a.strip()
 else:
  ans="NA"
 count=1
 info={}
 for resultID,scores in result.items():
  info['id_'+str(count)]=str(resultID)
  info['score_'+str(count)]=format(scores['cosineVal'],'.2f')
  count+=1
 del count
 result=jsonify({'response':ans,'info':info})
 return result
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
