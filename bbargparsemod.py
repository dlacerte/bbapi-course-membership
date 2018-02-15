##
# COMMAND LINE ARGUMENT PARSE MODULE for: bbapi-course-membership.py script
# Author: Dave Lacerte WCC Washtenaw Community College dlacerte@wccnet.edu
# Date: Feb 13 2018
# Modified: 
# DESCRIPTION: Process command-line arguments using argparse module: https://docs.python.org/2/howto/argparse.html
# ArgParse supports grouping of arguments = subparsers for each type of operation
# This script can perform the following operations on COURSE MEMBERSHIP records:
#
# 1) "update" the record: email, family-name, given-name, password, new-netid
# 2) "get" a single record that matches a given USERID
# 3) "list" all records matching a given USERID (or portion of a USERID string)
# 4) "delete" a single USERID from the COURSE
# 4.a) "purge" all USERID enrollment records from the course
# 5) "create" a new USERID enrollment record in the course
# Each operation has its own sub-parser and help example
# Added an optional -t TARGET option to specify TARGET BB INSTANCE for the commands:
# possible TARGETS are:  BBPROD9 = blackboard9.yourschool.edu
#                        BBPPRD9 = blackboard9-dev2.yourschool.edu
#                        PROD = your-prod.blackboard.com
#                        TEST = your-test.blackboard.com
#                        LIVE = your-live.blackboard.com (default)

import argparse
from bbconstants import *
global APIPATH
global FIELDS
global QTYPE


# FUNC: list_crs() List all USERID records matching the USERID (string pattern) that was provided
# The argparse subparsers refer to these functions
# Each function below builds the string/command that is sent to the various API endpoints
# Each function also defines the type of QUERY that is sent: GET, PUT, POST, PATCH, DELETE, (plus a custom PURGE type for deletion of multiple USERIDs)
# NOTE the API for COURSE MEMBERSHIP uses PUT instead of POST to create new membership/enrollment records
def list_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        FIELDS = ''
        APIPATH = crs_Path + crs_single_Path + args.courseid + crs_users_Path
        # Specifying FIELDS limits the value/params that are returned by the API call
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'GET'
# FUNC: purge_crs() remove/purge all USERID enrollmets from the given course
def purge_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        FIELDS = ''
        APIPATH = crs_Path + crs_courseid_Path + args.courseid + crs_users_Path
        # Specifying FIELDS limits the value/params that are returned by the API call
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'PURGE'
# FUNC: delete_crs() a single USERID record from the course (un-enroll one user)
def delete_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        FIELDS = ''
        APIPATH = crs_Path + crs_single_Path + args.courseid + crs_username_Path +  args.userid
        # Specifying FIELDS limits the value/params that are returned by the API call
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'DELETE'
# FUNC: update_crs() update a single USER enrollment record for the specified courseId/userId 
def update_crs(args):
        global APIPATH
        global FIELDS
        global QTYPE
        FIELDS = ''
        APIPATH  = crs_Path + crs_single_Path + args.courseid + crs_username_Path + args.userid
        # Specifying FIELDS limits the value/params that are returned by the API call
        #FIELDS = "&fields=courseId"
        QTYPE = 'PATCH'
# FUNC: create_crs() update a single USER enrollment record for the specified courseId/userId 
def create_crs(args):
        global APIPATH
        global FIELDS
        global QTYPE
        FIELDS = ''
        APIPATH  = crs_Path + crs_single_Path + args.courseid + crs_username_Path + args.userid
        # Specifying FIELDS limits the value/params that are returned by the API call
        #FIELDS = "&fields=courseId"
        QTYPE = 'PUT'
# FUNC: users_crs() List all USERID records matching the USERID (string pattern) that was provided
def users_crs(args):
        global APIPATH
        global FIELDS
        global QTYPE
        FIELDS = ''
        APIPATH  = crs_Path
        #APIPATH = APIPATH + crs_zero_offset_query
        APIPATH = APIPATH + crs_single_Path + args.courseid + crs_users_Path
        # Specifying FIELDS limits the value/params that are returned by the API call
        #FIELDS = "&fields=courseId"
        QTYPE = 'GET'

# FUNC: get_crs_users() GET a single COURSE record (not used) 
def get_crs_users(args):
        global APIPATH
        global FIELDS
        global QTYPE
        FIELDS = ''
        APIPATH  = crs_Path
        APIPATH = APIPATH + crs_single_Path + args.courseid + crs_users_Path
        #FIELDS = "?fields=userName,userId,created"
        QTYPE = 'GET'

def bbargs():
	parser = argparse.ArgumentParser(description='Process some command line Arguments')
	parser.add_argument('-t', '--target', help='-t TARGET_BB_INSTANCE: DEV2, PROD, SAAS, SAASTEST' )
	subparsers = parser.add_subparsers(help='operational commands: purge, list, update, create, delete, create')

# list all USER enrollments for a given courseid
	list_parser = subparsers.add_parser('list', help="list all enrollments for the courseId")
	list_parser.set_defaults(func=list_crs)
	list_parser.add_argument('courseid', action="store", help="courseId" )

# delete a single USER enrollment for a given courseid
	del_parser = subparsers.add_parser('delete', help="delete one enrollment user from courseId ")
	del_parser.set_defaults(func=delete_crs)
	del_parser.add_argument('courseid', action="store", help="courseId" )
	del_parser.add_argument('userid', action="store", help="userId" )

# purge all USER enrollments for a given courseid
	purge_parser = subparsers.add_parser('purge', help="purge all enrollments from courseId")
	purge_parser.set_defaults(func=purge_crs)
	purge_parser.add_argument('courseid', action="store", help="courseId" )

# update an existing USER enrollment record 
# the -a and -r options are optional aka required=False
	update_parser = subparsers.add_parser('update', help='update existing enrollment for courseId/userId' ) 
        update_parser.set_defaults(func=update_crs)
        update_parser.add_argument('courseid', action="store", help="courseId")
        update_parser.add_argument('userid', action="store", help="userId")
	update_parser.add_argument('-a', '--availability', action="store", help="availability for USERID (Yes/No)", required=False )
	update_parser.add_argument('-r', '--role', action="store", help="new role (Instructor/Student/Guest/TeachingAssistant/CourseBuilder/Grader)", required=False)

# Create a new USER enrollment record in the course
# To create a new enrollment both -a and -r options are required=True
	create_parser = subparsers.add_parser('create', help='create a new courseId/userId enrollment' ) 
        create_parser.set_defaults(func=create_crs)
        create_parser.add_argument('courseid', action="store", help="courseId")
        create_parser.add_argument('userid', action="store", help="userId")
	create_parser.add_argument('-a', '--availability', action="store", help="availability for USERID (Yes/No)", required=True )
	create_parser.add_argument('-r', '--role', action="store", help="new role (Instructor/Student/Guest/TeachingAssistant/CourseBuilder/Grader)", required=True)

        args = parser.parse_args()
#	print "ARGS =", args
        args.func(args)
        return args, APIPATH, FIELDS, QTYPE
