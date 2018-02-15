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
My development environment at WCC is a RHEL 7 server running Python 2.7 and a MobaXterm ssh terminal window. 
I was inspried to create this script (and others) after seeing Mark Kauffman https://github.com/mark-b-kauffman present a BB API demo 
at BB WORLD DevCon in New Orleans 2017
