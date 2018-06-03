## Incident Ticket Classifier
This utility will classify the incident tickets based on issue description

Prerequisite
-----------
This system was implemented and tested under Windows, Linux and Mac OS X with the following software 

+ Ubuntu 14.10.4 / Mac OS X 10.10 / Windows 10
+ Java 1.8.0 or higher (all system variables are set JAVA_HOME etc.)
+ Python 3.6 or higher
+ pip3 installation of python modules (numpy, scipy, sklearn, nltk, flask)
+ Download NLTK data
```
import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
>>> exit()
```

Usage
-----
+ Clone or download the [Miscellaneous repo](https://github.com/hmi-digital/Miscelleinious) and copy "IncidentClassifier" folder from "ServiceDesk" folder to D:/HMI folder (or your preferred location)
+ Ensure that you have following folder structure
+ IncidentClassifier
	+ config
	+ data
	+ model
	+ module
	+ classifyServer.py
	+ trainModel.py
+ Open command prompt, go to D:\HMI\IncidentClassifier folder and execute following command to run flask web server
```
$ python classifyServer.py
    WARNING - Training incident model...
	# Number of utterances for training: 12
	# Number of classes used in training: 3
 * Running on http://localhost:8001/ (Press CTRL+C to quit) 
```
+ Above command will train ML model and it will listen at port 8001 for user query

Configuration
-------------
+ Follow below mentioned steps to configure the Incident classifier
+ <h4>Training the model</h4>
+ You can train the model by providing all the variations of incidents in incidentTypes.json file located at (IncidentClassifier/data/incidents folder)
+ Provide the incident ticket class name in "name" JSON object and possible incident utterances in "utternces" JSON object
+ The model will be automatically trained while you run the flask web server
+ <h4>Threshold score</h4>
+ Once the model is trained in order to classify the correct class you can set threshold score i.e. Classifier.thresholdScore parameter in file located at (IncidentClassifier/config/classifier.properties file)
+ The server will return the class name only if confidence level is above the threshold score
+ <h4> Setting WebServer port</h4>
+ The port of flask webserver can be set by changing the SERVER_PORT parameter in file (IncidentClassifier/classifyServer.py file , line no 9)
+ Once the server is started , you can use REST API with following parameters
	+ Method - GET
	+ URL - ```http://localhost:<port>/classify?userUtterance=LEQM Issue```
	+ Response - ```{"class": "LEQMIssue","score": "0.71"}```

Contact
-------
helpdesk.hmilab@gmail.com
