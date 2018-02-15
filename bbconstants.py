# MODULE: bbconstants.py file for unchanging constants values
#

# The target App Servers also requires a registered RESTful API Integration definition
# These global variables should likely be in a centralized config file
dev2_appkey = 'XXXXXXX'
dev2_appsecret = 'XXXXXX'
dev2_app_server = "XXXXXXX.blackboard.com"
#
prod_appkey = 'XXXXXX'
prod_appsecret = 'XXXXXXX'
prod_app_server = "XXXXXX.blackboard.com"
#
saas_test_appkey = 'XXXXXXXXXXXXXXX'
saas_test_appsecret = 'XXXXXXXXXXXXXXXXXX'
saas_test_server = "XXXX.edu"
#
saas_prod_appkey = 'XXXXXXXXXXXXXXXXXXXXXXXX'
saas_prod_appsecret = 'XXXXXXXXXXXXXXXXXXXXXX'
saas_prod_server = "XXXXXXXXXXXX.blackboard.com"
#
saas_stage_appkey = 'XXXXXXXXXXXXXXXXXXXX'
saas_stage_appsecret = 'xxxxxxxxxxxxxxxxxxxxxx'
saas_stage_server = "XXXXX-stage.blackboard.com"
#
saas_live_appkey = 'XXXXXXXXXXXXXXXXXXX'
saas_live_appsecret = 'xxxxxxxxxxxxxxxxxxxxxxx'
saas_live_server = "XXXXXXXXXXXXXX-live.blackboard.com"
# All communication is via Secure HTTP https://
https = "https://"
# Use REQUESTS module to request access and optin the OAUTH2 authorization token
grant_request = { 'grant_type':'client_credentials' }
oauth_url = '/learn/api/public/v1/oauth2/token'
prox = { 'https': 'https://yourproxy.wccnet.edu:3128', 'http':'http://yourproxy.wccnet.edu:3128' }

# Path variables for building the API URL endpoint
crs_Path = '/learn/api/public/v1/courses'
crs_single_Path = '/externalId:'
crs_courseid_Path = '/courseId:'
crs_users_Path = '/users'
crs_single_user_Path = '/users/externalId:'
crs_username_Path = '/users/userName:'
