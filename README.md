# bbapi-course-membership.py
Command Line python script using API calls to create/delete/modify Blackboard Course enrollments
This script uses several python modules to accomplish sending BB Blackboard API requests to a BB SaaS/MH instance
It uses the Requests module for the HTTP/HTTPS connection to the API endpoints on the BB instances
It uses Argparse module to define the command-line arguments and command-line HELP menu
The Json module handles converting the JSON responses to/from JSON to/from Python dictionary/list objects
Python NEWB Disclaimer: 
One year ago I was hired as a LMS/Unix Admin at WCC Washtenaw Community College, after working for past 9+ years as
a hardware/software/networking break/fix post-sales support engineer at NETAPP (where I did almost Zero % programming ) 
Prior to NetApp I worked as a Systems Support Engineer at EDS and Sun Microsystems where I did some (Shell, PERL, C, C++ ) programming
and Oracle DB and Unix/Linux system administraion. Python is a new language for me (in the last 6 months) so the code presented here is
likely to contain things that will bother/upset more experienced Python folks, since it looks (to me) like PERL or Shell scripting.
The documentation in the code are really "notes to myself" as to what's going on in each section, hopefully you will find it useful.
I use lots of print statements to see what is happening at various steps, some of these are commented out now that I'm using the script in production, some I left in to give me assurance that the script did what I hoped it would do. 
My development environment at WCC is a RHEL 7 server running Python 2.7 and a MobaXterm ssh terminal window. 
I was inspried to create this script (and others) after seeing Mark Kauffman https://github.com/mark-b-kauffman present a BB API demo 
at BB WORLD DevCon in New Orleans 2017

Here are some examaples showing how I use this script as a BB/LMS admin: 

1a) My HELP menu/description: 
./bbapi-course-membership --help
usage: bbapi-course-membership [-h] [-t TARGET]
                               {purge,create,list,update,delete} ...
Process some command line Arguments
positional arguments:
  {purge,create,list,update,delete}
                        operational commands: purge, list, update, create,
                        delete, create
    list                list all enrollments for the courseId
    delete              delete one enrollment user from courseId
    purge               purge all enrollments from courseId
    update              update existing enrollment for courseId/userId
    create              create a new courseId/userId enrollment
optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        -t TARGET_BB_INSTANCE: DEV2, PROD, SAAS, SAASTEST

1) Add/Create a new user enrollment in a course as an Instructor: 
./bbapi-course-membership -t STAGE create CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18 dlacerte -a Yes -r Instructor
JSON string =  {"courseRoleId": "Instructor", "availability": {"available": "Yes"}}
STATUS_CODE: 201
STATUS_CODE: 201
RESULTS:  {u'created': u'2018-02-15T18:09:03.696Z', u'courseId': u'_72172_1', u'userId': u'_26297040_1', u'dataSourceId': u'_2_1', u'courseRoleId': u'Instructor', u'availability': {u'available': u'Yes'}}

2) List all enriollments for a course: 
./bbapi-course-membership -t STAGE list CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18
JSON string =  {}
https://wccnet-stage.blackboard.com/learn/api/public/v1/courses/externalId:CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18/users
{u'created': u'2018-02-15T18:11:29.845Z', u'courseId': u'_72172_1', u'userId': u'_9514422_1', u'dataSourceId': u'_2_1', u'courseRoleId': u'Grader', u'availability': {u'available': u'Yes'}}
{u'created': u'2018-02-15T18:09:03.696Z', u'courseId': u'_72172_1', u'userId': u'_26297040_1', u'dataSourceId': u'_2_1', u'courseRoleId': u'Instructor', u'availability': {u'available': u'Yes'}}
{u'created': u'2018-02-15T18:10:48.560Z', u'courseId': u'_72172_1', u'userId': u'_26297409_1', u'dataSourceId': u'_2_1', u'courseRoleId': u'Student', u'availability': {u'available': u'Yes'}}

3) Delete/un-enroll one USER from the course: 
./bbapi-course-membership -t STAGE delete  CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18  dlacerte_admin
JSON string =  {}
MY URL =  https://wccnet-stage.blackboard.com/learn/api/public/v1/courses/externalId:CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18/users/userName:dlacerte_admin
STATUS_CODE: 204

4) Purge ALL enrollments from a course: 
./bbapi-course-membership -t STAGE purge  CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18
JSON string =  {}
myURL =  https://wccnet-stage.blackboard.com/learn/api/public/v1/courses/courseId:CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18/users
Deleted User _9514422_1 from Course _72172_1
Deleted User _26297040_1 from Course _72172_1

5) Modify an enrollment record in a course to make a USERID Unavailable
./bbapi-course-membership -t STAGE update CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18 jllacerte -a No
JSON string =  {"availability": {"available": "No"}}
MY URL =  https://wccnet-stage.blackboard.com/learn/api/public/v1/courses/externalId:CRS-CPY-DO-NOT-USE-W_ACC-225-DL-D01-JD-W18/users/userName:jllacerte
STATUS_CODE: 200

