# -*- coding: utf-8 -*-
import os
import json
import re
import pickle
import codecs
import glob
import module as m
import sys
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
warnings.filterwarnings("ignore")
class faqModel:
 def __init__(self):
  print("\tTraining FAQ model...")
 def train(self):
  vectorDimension=200
  scriptDir=os.path.dirname(__file__)
  corpusPath=os.path.join(scriptDir,'data','domain','*.txt')
  listOfCorpusFiles=sorted(glob.glob(corpusPath))
  print("\tProcessing following Corpus files:",*listOfCorpusFiles,sep='\n\t')
  corpus=[]
  faq=[]
  for fileName in listOfCorpusFiles:
   corpusFile=codecs.open(fileName,'r',encoding='utf-8')
   corpus.append(corpusFile.read())
  faqPath=os.path.join(scriptDir,'data','faq','*.txt')
  listOfFaqFiles=sorted(glob.glob(faqPath))
  print("\n\tProcessing following FAQ files:",*listOfFaqFiles,sep='\n\t')
  for fileName in listOfFaqFiles:
   faqFile=codecs.open(fileName,'r',encoding='utf-8').read()
   i=1
   for line in faqFile.split('\n'):
    if(line.count('?')>1):
     print("\tSEVERE:Found multiple questions in %s at line %d."%(os.path.basename(fileName),i))
     print("\tSEVERE:Aborting the process..!!!")
     sys.exit("\tAborting...")
    line=line.replace('$','USD')
    line=line.replace('"','\'')
    que,ans=line.split('?')
    corpus.append(que+' ?')
    faq.append(line)
    i+=1
  print('\n\tTotal no of questions for training: %s'%len(corpus))
  stopListFile=os.path.join(scriptDir,'data','dictionary','stopwords_es.txt')
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
  stops=set(stopwords.words('spanish'))|extraStopWords
  tfidfVec=TfidfVectorizer(corpus,decode_error='ignore',stop_words=stops,ngram_range=(1,5),tokenizer=m.stemTokenize_2)
  trainsetIdfVectorizer=tfidfVec.fit_transform(corpus).toarray()
  vLength=len(trainsetIdfVectorizer[1])
  nDimension=vectorDimension
  if vLength<=vectorDimension:
   nDimension=vLength-1
  svd=TruncatedSVD(n_components=nDimension,algorithm='randomized',n_iter=15,random_state=42)
  trainLSA=svd.fit_transform(trainsetIdfVectorizer)
  picklePath=os.path.join(scriptDir,'model')
  fileName=os.path.join(picklePath,'corpus.m')
  fileObject=open(fileName,'wb')
  pickle.dump(corpus,fileObject)
  fileObject.close()
  fileName=os.path.join(picklePath,'faq.m')
  fileObject=open(fileName,'wb')
  pickle.dump(faq,fileObject)
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
 myModel=M()
 myModel.train()
if __name__=="__main__":
 main()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
