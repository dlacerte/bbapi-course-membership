#!/usr/bin/python -W ignore::DeprecationWarning

# PROGRAM: bbapi-course-membership
# Author: Dave Lacerte  Feb 12 2018 dlacerte@wccnet.edu 
# Modified: 
#
# Uses Blackboard REST API endpoint URLs to perform operations on COURSE MEMBERSHIP/USER records 
# Supported Operations are: 
# 1) "get" a single COURSE MEMBERSHIP record for a given course and given userid 
# 2) "list" all COURSE MEMBERSHIP records for a specified COURSEID
# 3) "update" a single COURSE MEMBERSHIP record with various parameters:
# 4) "create" a new COURSE MEMBERSHIP record for a given courseid and userid with various parameters:
# 5) "delete" a single COURSE MEMBERSHIP record for a given course and given userid ( un-enroll one user) 
# 6) "purge" all course membership/enrollments are deleted/purged from the course
# C

import json
import requests
import sys
import requests.packages.urllib3
import os
import pprint
from bbconstants import *
from bboauthmod import *

# this line forces python to ignore old/out-dated insecure urllib3 libs and un-verified http CERTS
requests.packages.urllib3.disable_warnings()

# Set PROXY environment variables so requests modules uses the proxy server
# Since balsa is behind the ASA firewall
os.environ["HTTPS_PROXY"] = 'https://yourproxy.edu:3128'
os.environ["HTTP_PROXY"] = 'http://yourproxy.edu:3128'

# There are five possible API QUERY types which can be sent to the API:
# GET - get a single or multiple COURSE MEMBERSHIP record(s)
# POST - create a new COURSE MEMBERSHIP record
# PATCH - update an existing COURSE MEMBERSHIP USER record 
# DELETE - delete a COURSE MEMBERSHIP USER record
# PUT - create new course membership user ( new user enrollment )
# Set the Default API Query type (initially) to an INVALID value
QTYPE = 'INVALID'

# process command line arguments passed to this script 
# Call the bbargs() function from the bbargparsemod module
from bbargparsemod import bbargs
args, APIPATH, FIELDS, QTYPE = bbargs()

# Define JSON INPUT strings for various POST/PATCH requests
# See: https://developer.blackboard.com/portal/displayApi for details or changes to the BB Api specs
# initial version of the script can change 6 items using six possible command line options after the COURSEID param
# This function strips out any keys in a dict which have no value paired with them (None values) 
def strip_None_keys(dict):
	for elem in dict.keys():
		if dict[elem] is False :
			del dict[elem]
	return dict

# create an empty User Input dictioanry (ui)
# there are two sub-dictionaries: 'name', 'availability' which are also empty
# INPUT JSON OBJECT looks like this: 
#{
#  "dataSourceId": "string",
#  "availability": {
#    "available": "Yes"
#  },
#  "courseRoleId": "Instructor"
#}
# assign command line arguments to the user_input dictionary key;value pairs
# create EMPTY dictionary, and any second-level dict to hold all possible command line input variables
ui = {}

# only build the User Input dict if we are creating/PUT or updating/PATCH a USER enrollment record 
# Add the key:value pairs into the EMPTY ui dict only if the value is not None
# PATCH = update existing USER Enrollment record
# PUT = create a new USER enrollment record
if QTYPE == 'PUT' or QTYPE == 'PATCH':
	ui['availability']={}
	if args.role is not  None :
		ui['courseRoleId'] = args.role
	if args.availability is not None :
		ui['availability']['available'] = args.availability

# call function to strip out any keys with values = None from the ui dict save to new ui_json_dict dictionary
# The resulting json_string is passed as DATA to the POST and PATCH API call
ui_json_dict = strip_None_keys(ui)
# ui_json_string is the DATA that we need to send to the API for either POST or PATCH methods
ui_json_string = json.dumps(ui_json_dict)
print "JSON string = ", ui_json_string
# END COMMAND LINE ARGUMENT PARSING 

# SELECT the chosen target BB system based on command line arguments provided
# BBPPRD9 XXXXX-dev2.yourschool.edu 
if args.target == 'BBPPRD9' or args.target == 'DEV2' :
	appkey = dev2_appkey
	appsecret = dev2_appsecret
	app_server = dev2_app_server

## PROD =  XXXX-prod.blackboard.com pre-production site 
elif args.target == 'PROD' or args.target == 'PROD' :
	appkey = prod_appkey
	appsecret = prod_appsecret
	app_server = prod_app_server
#
## LIVE = XXXXX-LIVE.blackboard.com SaaS site
elif args.target == 'LIVE' :
	appkey = saas_live_appkey
	appsecret = saas_live_appsecret
	app_server = saas_live_server

## TEST = XXXXXX-test.blackboard.com SaaS site
elif args.target == 'TEST' :
	appkey = saas_test_appkey
	appsecret = saas_test_appsecret
	app_server = saas_test_server
#
## STAGE = XXXXX-stage.blackboard.com SaaS site
elif args.target == 'STAGE' :
	appkey = saas_stage_appkey
	appsecret = saas_stage_appsecret
	app_server = saas_stage_server

## Print useage/error if appropraite TARGET is not specified
else : 
	#print "selecting default TARGET BB Instance BB LIVE "
	appkey = saas_live_appkey
        appsecret = saas_live_appsecret
        app_server = saas_live_server
#
## Print out the TARGET BB INSTANCE we are Working on
#print " ARGS.TARGET = ", args.target
#print "TARGET BB SYSTEM: ", app_server
###

# Establish a requests session with the target app_server 
# Call the bboauth() function from the bboauthmod module
# pass the sessionid (s), the app_server, appkey, appsecret, and proxy setting to the function
s = requests.session()
s.verify = False
result = bboauth(s, app_server, appkey, appsecret, prox)

#######################
# API FUNCTION Definitions 
#######################
# FUNC: apiget() accepts the SESSIONID, and the URI API endpoint to be queried using GET
# returns the results (dictionary) rapi
def apiget( bbsession, bburi ): 
     #print "Get USERID, CALL GET API function:", bburi
     rapi = bbsession.get( bburi )
     #decoded = rapi.json()
     #print "DECODED RES = ", decoded['results']
     #print "HEADERS = ", rapi.headers
     #print "LINK = ", rapi.links[ 'next']
     return rapi


# Call the API to obtain the initial set of data (records) which match the query string. 
# Print initial results and check if more PAGES of results are avaialble
# Using the QTYPE variable that was set based on the command line operation specified  
# Call the appropriate API function based on the QTYPE

# Here we delete ALL users enrolled in a course (including instructors, students, etc.) 
if QTYPE == 'PURGE' :
	# Issue API command to obtain a list of all USER/MEMBERSHIPS in the given course
        # Use GET to obtain the list of course member/enrollments (if any) 
	myurl = https + app_server + APIPATH 
        print "myURL = ", myurl
        QTYPE = 'GET'
        # GET a list of enrollments for the given course
	response = s.request(QTYPE, myurl, proxies=prox) 
        resp_json = response.json()
        #print "RESP JSON = ", resp_json
        #print "RESP JSON = ", resp_json['results']
        #print "RESP JSON = ", resp_json['results']
        #print "LENGTH RESP JSON = ", len(resp_json['results'])
        if len(resp_json['results']) > 0 :
        	list_page = resp_json['results']
                # loop through the results and delete each userId from the course with an API call
                # x contains a dictionary for each results record, we extract values from results using the 'userId' and 'courseID' keys
                for x in list_page:
                	CID = x['courseId']
 			UID = x['userId']
                        myurl = https + app_server + crs_Path + '/' + CID + crs_users_Path + '/' +  UID
                        # Call the  API endpoint to DELETE the (UID) USER/MEMBERSHIP from the (CID) COURSE
        		QTYPE = 'DELETE'
                        response = s.request(QTYPE, myurl, proxies=prox)  
        		#print "My URL for deletion: ", myurl

	# STATUS CODE 204 is returned for a successful DELETE operation
        # Output JSON is only generated for deletion errors
        # Other possible codes: 400=invalid userid, 403=auth problem, 404=not found
		        if response.status_code == 204 : 
        			#print("DELETED STATUS CODE: " + str(response.status_code))
                                print("Deleted User " + UID + " from Course " + CID)
        		else: 
         			resp_json = response.json()
                		print ("STATUS_CODE: " + str(response.status_code))
                		print "RESPONSE: ", resp_json
	else: 
		print "No course enrollments to delete"
		
# DELETE one user enrollment 
elif QTYPE == 'DELETE' :
         myurl = https + app_server + APIPATH 
         print "MY URL = ", myurl
         #myheaders = {'content-type':'application/json'}
         #response = s.request(QTYPE, myurl, data=patchdata, headers=myheaders, proxies=prox )
         response = s.request(QTYPE, myurl, proxies=prox )
         # Check is STATUS_CODE is OK (less then 400)
         # A successful DELETE request should return a STATUS-CODE = 204 
         # Output JSON is only generated for PATCH errors
         # Other possible codes: 400=incorrect parameters specified, 403=auth problem, 404=userid not found, 409=duplicate batchuid or username exists
         if response.ok : 
         	print("STATUS_CODE: " + str(response.status_code))
         	#print("STATUS_CODE: " + str(response.text))
         else: 
         	resp_json = response.json()
                print ("STATUS_CODE: " + str(response.status_code))
                print "RESPONSE: ", resp_json

# PATCH/update an existing course membership record
elif QTYPE == 'PATCH' :
	 patchdata = ui_json_string
         myurl = https + app_server + APIPATH 
         print "MY URL = ", myurl
         myheaders = {'content-type':'application/json'}
         response = s.request(QTYPE, myurl, data=patchdata, headers=myheaders, proxies=prox )
         # Check is STATUS_CODE is OK (less then 400)
         # A successful PATCH request should return a STATUS-CODE = 200 
         # Output JSON is only generated for PATCH errors
         # Other possible codes: 400=incorrect parameters specified, 403=auth problem, 404=userid not found, 409=duplicate batchuid or username exists
         if response.ok : 
         	print("STATUS_CODE: " + str(response.status_code))
         	#print("STATUS_CODE: " + str(response.text))
         else: 
         	resp_json = response.json()
                print ("STATUS_CODE: " + str(response.status_code))
                print "RESPONSE: ", resp_json

# PUT/create a new course membership record
elif QTYPE == 'PUT' :
         postdata = ui_json_string
         myurl = https + app_server + APIPATH 
         myheaders = {'content-type':'application/json'}
         #print "my Data: ", patchdata
         response = s.request(QTYPE, myurl, data=postdata, headers=myheaders, proxies=prox )
         # Check if STATUS_CODE is OK (less than 400)  
         # STATUS_CODE = 201 is returned when a new USERID is created via POST
         # Other possible codes:  400=error occurred, 403=Auth error, 409=USERID already exists
	 if response.ok :
                print("STATUS_CODE: " + str(response.status_code))
         else:
                resp_json = response.json()
                print ("STATUS CODE: " + str(response.status_code))
                print "RESPONSE: ", resp_json

         resp_json = response.json()
         print("STATUS_CODE: " + str(response.status_code))
         print "RESULTS: ",  resp_json

else:
        # Default operation is a GET
        
        print https + app_server + APIPATH + FIELDS 
	response = apiget(s, https + app_server + APIPATH + FIELDS )
        resp_json = response.json()
        #print "STATUS_CODE: ",  str(response.status_code)
        #print "RESULTS: \n ",  json.dumps(resp_json)
	#print "STATUS_CODE: ",  str(response.status_code)
        #print "HEADER = ", str(response.headers)
        #print "TEXT = ", str(response.text)
        #print "RESP = ", str(response.json())
        #print "ENCODING = ", str(response.encoding)
        #print "RESULTS: \n ",  json.dumps(resp_json)

# If the JSON response includes paging info we need to interate over all of the avaialble pages ( with more requests for page offsets) to fetch ALL data records
# If paging data is NOT present then we have recieved all of the data records and this loop is NOT entered
	while resp_json.has_key('paging'):
        	#path,params = next_page.split("?")
        	#fields,match,page = params.split("&")
        	#next_page = path + "?" + page + "&" + match + "&" + fields 
        	list_page = resp_json['results']
        	#print "NEXT PAGE RESULTS: ", resp_json['results']
 	        for x in list_page:
                    print x
                # get the next page worth of data via another API call (fetch next page)
                next_page = resp_json['paging']['nextPage']
                response = apiget(s, https + app_server + next_page)
                resp_json = response.json()
                #print "NEXT page orig: ", next_page

# If only a single page of data is returned it will not include a 'paging' designation, but it may include multiple records in the 'results'
        else :
                if resp_json.has_key('results'):
                        list_page = resp_json['results']
                        for x in list_page:
                                print x
# A single record might be returned in the response, print it out
                else:
                        print resp_json
                        #print resp_json.keys()
                        #print resp_json.values()
