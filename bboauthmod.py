# FUNCTION: bboauth() calls REST API to obtain OAUTH TOKEN for a given Blackboard Target Server URL
# This script uses the REQUESTS/SESSIONS python module:
# http://docs.python-requests.org/en/master/user/advanced/#session-objects
# establish an initial https session which will remain OPEN for reuse, multiple GET or POST requests
# First order of business it to obtain an authorization token from the BB DEVELOPER PORTAL:
# https://developer.blackboard.com/
# Once AUTH TOKEN is retrieved it is stored in the OPEN session header object/property
import requests 
import json
from bbconstants import *

def bboauth(s, bbtarget, appkey, appsecret, prox):

	# Create an empty dictionary obect to store the records returned by the requests sent to the API endpoint
	data_set = []
        oauth_endpoint = 'https://' + bbtarget + oauth_url

	#Call post method in the session to request the AUTH TOKEN to be used for remainder of session
	r = s.post(oauth_endpoint, data=grant_request, auth=(appkey, appsecret), proxies=prox )
	#print("STATUS CODE: " + str(r.status_code))
	#print("RESPONSE: " + r.text)

	# if we get a good (200) response display the auth token
	# and store the AUTH TOKEN into the OPEN session header property
	# otherwise exit since Auth Token was not granted for some reason
	if r.status_code == 200:
        	parsed_json = json.loads(r.text)
        	token = parsed_json['access_token']
        	#print("AUTH TOKEN: " + token )
        	# Assign the aquired AUTH TOKEN to the session header for repeated use in subsequent session calls
        	authStr = 'Bearer ' + token
        	s.headers.update({'Authorization': authStr } )
	else:
     		print("EXIT: Auth Token Request Failed")
     		exit
	return authStr
