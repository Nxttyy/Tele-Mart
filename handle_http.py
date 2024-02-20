# importing the requests library
import requests
 
from dotenv import load_dotenv
import os
 
# Load environment variables from the .env file
load_dotenv()
 
token = os.getenv("TOKEN")
# api-endpoint
# URL = "http://maps.googleapis.com/maps/api/geocode/json"
 
# location given here
# location = "delhi technological university"
 
# defining a params dict for the parameters to be sent to the API
PARAMS = {}
 
# sending get request and saving the response as response object
# r = requests.get(url = URL, params = PARAMS)
 
# extracting data in json format
# data = r.json()

def get_update_http():
	url = "https://api.telegram.org/bot"+ token +"/getUpdates"
	r = requests.get(url = url, params = PARAMS)
	data = r.json()

	return data

def send_to_chat():
	url = "https://api.telegram.org/bot"+ token + "/sendMessage"
	PARAMS = {'chat_id':,
				'text':'Hello Chat.'}

	# print(data)
