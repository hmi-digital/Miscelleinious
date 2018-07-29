## Intent Classifier
This utility will classify the intent based on end user utterance

Prerequisite
-----------
This system was implemented and tested under Windows, Linux and Mac OS X with the following software 

+ Ubuntu 14.10.4 / Mac OS X 10.10 / Windows 10
+ Java 1.8.0 or higher (all system variables are set JAVA_HOME etc.)
+ Python 3.6 or higher
+ pip3 installation of python modules (numpy, scipy, keras, spacy, h5py, flask)
+ Sapcy english model

```
$python -m spacy.en.download all

```

Usage
-----
+ Clone or download the [Miscellaneous repo](https://github.com/hmi-digital/Miscelleinious) and copy "IntentClassifier" folder to D:/HMI folder (or your preferred location)
+ Ensure that you have following folder structure
+ IncidentClassifier
	+ config
	+ data
	+ log
	+ model
	+ module
	+ classifyServer.py
+ Open command prompt, go to D:\HMI\IntentClassifier folder and execute following command to run flask web server
```
$ python classifyServer.py
Loading english trained model...
...done
WARNING - Training intent model...
.
.
.
 * Running on http://localhost:8001/ (Press CTRL+C to quit)
```
+ Above command will train intent model and will listen at port 8001 for user query

Configuration
-------------
+ Follow below mentioned steps to configure the Intent classifier
1. <h4>Training the model</h4>
+ You can train the model by providing train and test data in intent.json file located at (IntentClassifier/data/train and IntentClassifier/data/test folder repectively)
+ Add couple of samples for each intent class in test data so that CNN module can be trained with good accuracy.
+ Provide the intent name in "name" JSON object and possible utterances in "utternces" JSON object. (see sample intent.json provided)
+ The model will be automatically trained while you run the flask web server
2. <h4>Threshold score</h4>
+ Once the model is trained in order to classify the correct intent class you can set threshold score i.e. Classifier.thresholdScore parameter in file located at (IntentClassifier/config/classifier.properties file)
+ The server will return the class name only if confidence level is above the threshold score
3. <h4>Failure Logs</h4>
+ The logs will be avialable at (IntentClassifier/log) where all the utterances which were not able to classify are logged.
+ Note that log stores the original utterance as recieved by user ,probability score and closest class that it could match.
4. <h4> Setting WebServer port</h4>
+ The port of flask webserver can be set by changing the SERVER_PORT parameter in file (IntentClassifier/classifyServer.py file , line no 8)
+ Once the server is started , you can use REST API with following parameters
	+ Method - GET
	+ URL - ```http://localhost:<port>/classify?userUtterance=How is% weather```
	+ Response - ```{"intent":"getWeatherInformation","score":"0.81","text":"How is weather"}```

Contact
-------
helpdesk.hmilab@gmail.com
