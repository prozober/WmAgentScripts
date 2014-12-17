#!/usr/bin/python -u

from datetime import datetime

import sys,os

print "Content-type: text/html\n"

import cgi,sys
form = cgi.FieldStorage()

f = open("relval_batch_assigner_logs/log.dat", 'a')

f.write(str(datetime.now())+": "+str(form)+"\n")
f.flush()

title=form["AnnouncementTitle"].value
wfs=form["ListOfWorkflows"].value.split('\n')
procver=form["ProcessingVersion"].value
site = form["Site"].value
if 'Test' in form:
    test = True
else:
    test = False
statistics_fname = form["StatisticsFilename"].value
hnpost = form["HypernewsPost"].value
description = form["Description"].value

print "Description: "+description
print "<br>"
print "Hypernews Post: "+hnpost
print "<br>"
print "StatisticsFilename: "+statistics_fname
print "<br>"
print "Announcement e-mail title: "+title
print "<br>"
print "Site: "+site
print "<br>"
print "Processing version: "+procver
print "<br>"
print "Workflows:"
print "<br>"
for wf in wfs:
    wf = wf.rstrip('\n')
    wf = wf.rstrip('\r')
    if wf.strip() == "":
        continue
    print wf
    print "<br>"
print "Test: "+str(test)
print "<br>"

wf_names_fname=os.popen("mktemp").read()
wf_names_fname=wf_names_fname.rstrip('\n')
wf_names_fname=wf_names_fname.rstrip('\r')

for wf in wfs:
    wf = wf.rstrip('\n')
    wf = wf.rstrip('\r')
    if wf.strip() == "":
        continue
    os.system("echo "+wf+" >> "+wf_names_fname)

if test:
    sys.exit(0)

os.system("echo python2.6 insert_batch.py "+hnpost+" "+wf_names_fname+" \""+title+"\" "+statistics_fname+" \""+description+"\" "+procver+" "+site+" >> relval_batch_assigner_logs/log.dat")

os.system("python2.6 insert_batch.py "+hnpost+" "+wf_names_fname+" \""+title+"\" "+statistics_fname+" \""+description+"\" "+procver+" "+site+";")

#os.popen("cat brm/log.dat | mail -s \"[RelVal] "+ title +"\" hn-cms-hnTest@cern.ch -- -f amlevin@mit.edu");
os.popen("echo "+description+" | mail -s \"[RelVal] "+ title +"\" andrew.m.levin@vanderbilt.edu -- -f amlevin@mit.edu");    


