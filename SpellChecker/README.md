## Tool to auto correct your utterance to correct spelling
This utility will provide REST based API for auto correcting your utterance using spellchecker module.

Prerequisite
-----------
This system was implemented and tested under Windows, Linux and Mac OS X with the following software 

+ Ubuntu 14.10.4 / Mac OS X 10.10 / Windows 10
+ Python 3.6 or higher
+ pip3 installation of python modules (pyspellchecker, flask)


Usage
-----
+ Clone or download the [Miscellaneous repo](https://github.com/hmi-digital/Miscelleinious) and copy "SpellChecker" folder to D:/HMI folder (or your preferred location).
+ Ensure that you have following folder structure
+ SpellChecker
	+ data
	+ module
	+ app.py
+ Create your custom dictionary by adding custom words in dictionary.txt located in ./data/ folder.
+ Open command prompt, go to D:\HMI\SpellChecker folder and execute following command to run flask web server.
```
$ python app.py
.
.
.
 * Running on http://localhost:8001/ (Press CTRL+C to quit)
```
+ Above command will now will listen at port 8001 for user query

Configuration
-------------
1. <h4> Setting WebServer port</h4>
+ The port of flask webserver can be set by changing the SERVER_PORT parameter in file (SpellChecker/app.py file , line no 9)
+ Once the server is started , you can use REST API with following parameters
	+ Method - GET
	+ URL - ```http://localhost:<port>/spellCheck```
	+ URL Parameter
		+ ```utterance=Log in to competer```
	+ Try the same URL in browser e.g. ```http://127.0.0.1:8001/spellCheck?utterance=Log%20in%20to%20competer```
	+ Response - ```{"Utterance":"log in to computer"}```
+ You can get required data by changing your utterance in url parameter.

