### Tweets Webapp


Run this app from the project directory:  

    python3 app.py

Run the tests from the project directory: 

    python3 -m pytest
    
If requirements are missing, install **requirements.txt** from the project directory. Suggestion: 

    pip install -r requirements.txt

IMPORTANT: You must change the consumer_key and consumer_secret in the config.json for this to work 

## app 

This app makes calls to two Twitter endpoints: 

1. [Oauth2](https://developer.twitter.com/en/docs/basics/authentication/api-reference/token) endpoint for authenticating with my twitter account key/secret pair. *Note: just for demonstration. It is otherwise not good practice to include my secret keys in the code.*

2. Twitter [search](https://developer.twitter.com/en/docs/tweets/search/overview/basic-search) endpoint for pulling twitter's recent tweets with hashtag defined in config. Currenlty set to #telaviv 

The json returned contains a list of posts under key "statuses". The relevant data is added to a dict of tweet info, and appended to a list of 20 items which are rendered to the html page. Clicking on the item opens a tab for the original tweet. 



## implementation 

The app is pretty basic. Python and Flask for the server and HTML/jinja on the front-end. 
I felt it would be over-engineering to use JS, although I did consider it for the pagination. 

The decision I faced was whether to make a new call for each page load, but given the nature of twitter and how often I saw new tweets come in, 
I wanted the accuracy of getting the latest data in real-time


## config 

Urls and constants, such as item-per-page-limit and which hashtag to use, are defined in the config.json file