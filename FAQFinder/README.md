## FAQ answer finder
This utility will identify the best matching answer to standard FAQ's based on query description given by user.

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
+ Clone or download the [Miscellaneous repo](https://github.com/hmi-digital/Miscelleinious) and copy "FAQFinder_\<language\>" folder from "FAQFinder" folder to D:/HMI folder (or your preferred location)
+ Ensure that you have following folder structure
+ FAQFInder_\<language\>
	+ config
	+ data
	+ model
	+ module
	+ log
	+ faqFinderServer.py
	+ trainModel.py
+ Open command prompt, go to D:\HMI\FAQFinder_\<language\> folder and execute following command to run flask web server
```
$ python faqFinderServer.py
    Training FAQ model...
	Processing following Corpus files:
	X
	Processing following FAQ files:
	X
	Total no of questions for training: 50
 * Running on http://localhost:8001/ (Press CTRL+C to quit) 
```
+ Above command will train faqModel ML model and it will listen at port 8001 for user query

Configuration
-------------
+ Follow below mentioned steps to configure the FAQFinder service
1. <h4>Training the model</h4>
+ You can train the model by providing domain corpus (content that describes the domain ~ 20-30 lines) in corpus_X.txt file located at (FAQFinder_<language>/data/domain folder)
+ Provide the standard set of Questions and Answers in faq_X.txt (you can add many files as you want based on different categories) file located at (FAQFinder_<language>/data/faq folder)
+ <b>Important :</b>The format for entering standard questions answer is \<question\> ? \<answer\> without any line breaks.
+ The model will be automatically trained while you run the flask web server
2. <h4>Threshold score</h4>
+ Once the model is trained in order to find the best matching answer you can set threshold score i.e. finder.thresholdScore parameter in file located at (FAQFinder_\<language\>/config/faqFinder.properties file)
+ The server will return the answer name only if confidence level is above the threshold score
3. <h4>Similarity Index</h4>
+ If there are multiple answers to the given question that exceeds threshold score , the JSON response will also suggest those answers. The answer will be included to response only if the next best answer is within the similarity index score. (e.g. if threshold score is 0.4 and similarity index is 0.2, then the response will include answer with score 0.7 (as it exceeds 0.4) but not the answer with 0.45 (though it is more than the threshold score, it is not within the similarity index of 0.2 - here we get similarity index or closeness score of 0.25)
+ You can set the similarity index i.e. finder.similarityIndex parameter in file located at (FAQFinder_\<language\>/config/faqFinder.properties file)
4. <h4>Failure Logs</h4>
+ The FAQFinder server will log the questions that it had failed to answer. This will help you either refine the existing questions or add the missing questions to your list.
+ You can check month-wise log located at FAQFinder_\<language\>/log/\<month\>_training.txt The log file will be auto purged.
5. <h4> Setting WebServer port</h4>
+ The port of flask webserver can be set by changing the SERVER_PORT parameter in file (FAQFinder_\<language\>/faqFinderServer.py file , line no 9)
+ Once the server is started , you can use REST API with following parameters
	+ Method - GET
	+ URL - ```http://localhost:<port>/faq?userUtterance=What is ATM ?```
	+ Response - ```{
    			"info": {
        		"id_1": "2",
       	 		"id_2": "49",
        		"score_1": "0.62",
        		"score_2": "0.43"
    			},
    			"response": "ATM is cash withdrawl machine."
			}```
