## API End Point to CSV Database
This utility will provide API based access to different CSV data (located in \data folder). You can filter the specific data by changing your query.

Prerequisite
-----------
This system was implemented and tested under Windows, Linux and Mac OS X with the following software 

+ Ubuntu 14.10.4 / Mac OS X 10.10 / Windows 10
+ Python 3.6 or higher
+ pip3 installation of python modules (numpy, pandas, flask)


Usage
-----
+ Clone or download the [Miscellaneous repo](https://github.com/hmi-digital/Miscelleinious) and copy "APIEndPoint" folder to D:/HMI folder (or your preferred location).
+ Ensure that you have following folder structure
+ APIEndPoint
	+ data
	+ module
	+ app.py
+ Open command prompt, go to D:\HMI\APIEndPoint folder and execute following command to run flask web server.
+ It will poll the data folder every 10 sec. So feel free to add,change,modify data to this folder.
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
+ The port of flask webserver can be set by changing the SERVER_PORT parameter in file (APIEndPoint/app.py file , line no 11)
+ Once the server is started , you can use REST API with following parameters
	+ Method - GET
	+ URL - ```http://localhost:<port>/getData```
	+ URL Parameter
		+ ```source = customer```
		+ ```query = Name=='Allen'&Credit_Limit>4000```
	+ Try the same URL in browser e.g. ```http://127.0.0.1:8001/getData?source=customer&query=Name==%27John%27%26Credit_Limit%3E4000```
	+ Response - ```{"2":{"Id":100002,"Name":"Allen","Account_Number":1608900127,"Credit_Card_Number":4544150000009750,"Credit_Limit":10000,"Credit_Balance":9500,"Customer_Profile":"High_Risk"},"3":{"Id":100002,"Name":"Allen","Account_Number":1608900128,"Credit_Card_Number":4544150000003971,"Credit_Limit":15000,"Credit_Balance":15000,"Customer_Profile":"High_Risk"}}```
+ You can get required data by changing your query in url parameter.
