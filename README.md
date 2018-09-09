# Perforce-SCM
To build Python Automation script to do SCM in Perforce

Prerequisites:
Perforce SCM - www.perforce.com – there is a free version that allows us to run it locally for small number of users w/o any additional registration/costs, it also has means of automation

Task accomplished by this automation:

1. Read config file. This file will contain following settings:
a. For mail delivery (SMTP)
b. For access to perforce server

2.Get from perforce a list of changes (changelists with comments) made since last script run time and get all updated files

3.Get from perforce a list of changes (changelists with comments) made since last script run time and get all updated files

4.If running of build script is successful, add/update contents of the folder named ‘bin’ in the perforce repository

5.In case of execution error, send out an email with the list of changes retrieved in p.2 and all outputs of build script (both stdout/stderr)

Run Instructions:

Provide appropriate parameters in the config.ini file. Sample config.ini is attached here for help in Samples.zip.
Create a folder structure under depot and place task.bat file in this path    
        (depot -try -> task.bat)
Run Build.py
If current revision of the build in workspace is less than the latest revision then this script will update it to latest revision.
task.bat will be executed as part of Build.py.
It will create a folder named ‘BuildAction’ in the same path as that of task.bat. Folder creation should be considered as build action or result.
In case ‘BuildAction’ already exists, then a build failure notification will be sent to the receiver email ID along with Changelist starting from last revision till the latest.

Assumption:
Sender email Id will be a Gmail ID as  SMTP server for Gmail has been used
Build.py and Config.ini are placed in same path in local system
