from os import listdir
from os.path import isfile,join,splitext
import pandas as pd
import time, threading

#after this interval it will reread the source data
WAIT_SECONDS = 10

DATA_SOURCE ='./data/'
dataDict = {}
datafiles = [f for f in listdir(DATA_SOURCE) if isfile(join(DATA_SOURCE, f))]

# read data from all the sources
def readData():
# list of data sources
    for f in datafiles:
        print("=============== Periodic reading of data from source: " + f)
        # reading data frame from csv file
        dataDict[splitext(f)[0]] = pd.read_csv(DATA_SOURCE + f, sep=',')
    threading.Timer(WAIT_SECONDS, readData).start()