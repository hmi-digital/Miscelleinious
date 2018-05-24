# -*- coding: utf-8 -*-
import os
import json
import re
import pickle
import codecs
import module as m
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
class incidentModel:
 def __init__(self):
  print("\tWARNING - Training incident model...")
 def train(self):
  vectorDimension=200
  scriptDir=os.path.dirname(__file__)
  fileData=os.path.join(scriptDir,'data','incidents','issueTypes.json')
  utterance=[]
  classes=[]
  with codecs.open(fileData,'r','utf-8')as dataFile:
   data=json.load(dataFile)
  for nameUtterances in data['classes']:
   for utt in nameUtterances['utterances']:
    utterance.append(utt)
    classes.append(nameUtterances['name'])
  myClasses=set(classes)
  print('\t# Number of utterances for training:',len(utterance))
  print('\t# Number of classes used in training:',len(myClasses))
  stopListFile=os.path.join(scriptDir,'data','dictionary','stopwords_en.txt')
  arrayWords=[]
  stopWords=[]
  f=codecs.open(stopListFile,'r','utf-8')
  lines=f.read().split("\n")
  for line in lines:
   if line!="":
    arrayWords.append(line.split(','))
  for a_word in arrayWords:
   for s_word in a_word:
    if(re.sub(' ','',s_word))!="":
     stopWords.append(s_word)
  extraStopWords=set(stopWords)
  stops=set(stopwords.words('english'))|extraStopWords
  tfidfVec=TfidfVectorizer(utterance,decode_error='ignore',stop_words=stops,ngram_range=(1,5),tokenizer=m.stemTokenize_2)
  trainsetIdfVectorizer=tfidfVec.fit_transform(utterance).toarray()
  vLength=len(trainsetIdfVectorizer[1])
  nDimension=vectorDimension
  if vLength<=vectorDimension:
   nDimension=vLength-1
  svd=TruncatedSVD(n_components=nDimension,algorithm='randomized',n_iter=15,random_state=42)
  trainLSA=svd.fit_transform(trainsetIdfVectorizer)
  picklePath=os.path.join(scriptDir,'model')
  fileName=os.path.join(picklePath,'utterance.m')
  fileObject=open(fileName,'wb')
  pickle.dump(utterance,fileObject)
  fileObject.close()
  fileName=os.path.join(picklePath,'classes.m')
  fileObject=open(fileName,'wb')
  pickle.dump(classes,fileObject)
  fileObject.close()
  fileName=os.path.join(picklePath,'tfidfVec.m')
  fileObject=open(fileName,'wb')
  pickle.dump(tfidfVec,fileObject)
  fileObject.close()
  fileName=os.path.join(picklePath,'svd.m')
  fileObject=open(fileName,'wb')
  pickle.dump(svd,fileObject)
  fileObject.close()
  fileName=os.path.join(picklePath,'trainLSA.m')
  fileObject=open(fileName,'wb')
  pickle.dump(trainLSA,fileObject)
  fileObject.close()
def main():
 myModel=incidentModel()
 myModel.train()
if __name__=="__main__":
 main()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
