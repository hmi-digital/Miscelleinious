## API End Point to CSV Database
This utility will provide API based access to CSV data (located in \data folder). You can filter the specific data by changing the query.

Prerequisite
-----------
This system was implemented and tested under Windows, Linux and Mac OS X with the following software 

+ Ubuntu 14.10.4 / Mac OS X 10.10 / Windows 10
+ Python 3.6 or higher
+ pip3 installation of python modules (numpy, pandas, flask)


Usage
-----
+ Clone or download the [Miscellaneous repo](https://github.com/hmi-digital/Miscelleinious) and copy "APIEndPoint" folder to D:/HMI folder (or your preferred location)
+ Ensure that you have following folder structure
+ APIEndPoint
	+ data
	+ app.py
+ Open command prompt, go to D:\HMI\APIEndPoint folder and execute following command to run flask web server
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
+ The port of flask webserver can be set by changing the SERVER_PORT parameter in file (APIEndPoint/app.py file , line no 9)
+ Once the server is started , you can use REST API with following parameters
	+ Method - GET
	+ URL - ```http://localhost:<port>/params/Name=='John'&Credit_Limit>=0```
	+ Response - ```{"Id":{"0":100001,"1":100001},"Name":{"0":"John","1":"John"},"Account_Number":{"0":1608900125,"1":1608900125},"Credit_Card_Number":{"0":4544150000004734,"1":4544150000003765},"Credit_Limit":{"0":0,"1":5000},"Customer_Profile":{"0":"Low_Risk","1":"Low_Risk"}}```
+ You can get required data by changing your query in url parameter.

Contact
-------
helpdesk.hmilab@gmail.com
