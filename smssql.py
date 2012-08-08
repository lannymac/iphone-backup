#! /usr/bin/python

from datetime import datetime
from time import *
from collections import Counter
import pylab as plt
import pylab as pl
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import sqlite3
import os
import sms as smsclass
from getpass import getuser
import pickle
from sms import sms as smsclass
import re



def todatenum(d):
    # d is a datetime.datetime or a datetime.time object
    try: d1=d.toordinal()
    except: d1=0
    d2=(d.hour+(d.minute+d.second/60.)/60.)/24.
    dn=d1+d2
    return dn

def searchchar(string,char):
    output=False
    if string != None:
        for i in range(len(string)):
            if string[i]==char:
                output=True
    return output
            

q1=raw_input("Would you like to open and append to a previously loaded database?  ")
if q1=='y':
    q1a=raw_input("Enter the location of this file:\n")
    smsdb=pickle.load(open(q1a,"rb"))
    databaseq='y'
if q1=='n':
    databaseq='n'

q5=raw_input("In order for this program to work, you must specify a place where\
 the sms and contact SQL database files will be stored:   ")
if q5[-1]!="/":
    q5=q5+"/"

print("\n")
print("You will now be given a choice as to which folder you would like to use to \
extract the messages. Each folder corresponds to a backup for a particular Apple device. \
There is no easy way to know which folder is the correct one. Trial and error seems \
to be the best way to do this. Choose a folder and if it doesn't work, \
restart the program and try again\n")


backupdirs=[name for name in os.listdir("/Users/"+getuser()+"/Library/Application Support/MobileSync/Backup/")]

for i in range(len(backupdirs)):
    if backupdirs[len(backupdirs)-1-i][0]==".":
        del backupdirs[len(backupdirs)-1-i]

for i in range(len(backupdirs)):
    print(str(i)+" - "+backupdirs[i])


print("\n")
q3=raw_input("Enter the number corresponding to the backup folder you would like to use:  ")

os.system("cp /Users/landan/Library/Application\ Support/MobileSync/Backup/"+backupdirs[int(q3)]+\
"/3d0d7e5fb2ce288813306e4d4636395e047a3d28 "+str(q5)+"sms.db")
smsDB= sqlite3.connect("DataBaseFiles/sms.db")

with smsDB:
    cur = smsDB.cursor()
    cur.execute("SELECT * FROM message")

    sms = cur. fetchall()

        
#####READ IN ADDRESS BOOK######
os.system("cp /Users/landan/Library/Application\ Support/MobileSync/Backup/"+backupdirs[int(q3)]+\
"/31bb7ba8914766d4ba40d6dfb6113c8b614be442 "+str(q5)+"contacts.db")

Addy=sqlite3.connect("DataBaseFiles/contacts.db")
with Addy:
    cur = Addy.cursor()
    cur.execute("SELECT * FROM ABPerson")
    
    address = cur.fetchall()
contacts=[]
for i in range(len(address)):
    tempdict={"ROWID":address[i][0],"First":address[i][1],"Last":address[i][2]}
    contacts.append(tempdict)

with Addy:
    cur.execute("SELECT * FROM ABMultiValue")
    phonenums=cur.fetchall()

addresses=[]
for i in range(len(phonenums)):
    tempdict={"ROWID":phonenums[i][1],"Address":phonenums[i][5]}
    addresses.append(tempdict)

for i in range(len(contacts)):
    contacts[i]["Address"]=[]

for i in range(len(addresses)):
    tempID=addresses[i]["ROWID"]
    for j in range(len(contacts)):
        if tempID==contacts[j]["ROWID"]:
            contacts[j]["Address"].append(addresses[i]["Address"])

for i in range(len(contacts)):
    for j in range(len(contacts[i]["Address"])):
        tempstring=contacts[i]["Address"][j]
        try:
            tempstring=re.sub("[^0-9]","",tempstring)
            if tempstring[0] != u'1':
                tempstring=u'1'+tempstring
            tempstring=u'+'+tempstring
            contacts[i]["Address"][j]=tempstring
        except:
            pass


##############################


sms_database=[]
sms_database.append(contacts)
for i in range(len(sms)):
    if sms[i][4]==2 or sms[i][4]==3:
        tempnum=sms[i][1]
        try:
            tempnum=re.sub("[^0-9]","",tempnum)
            if tempnum[0] != u'1':
                tempnum=u'1'+tempnum
            tempnum=u'+'+tempnum
        except:
            pass

        for j in range(len(contacts)):
            for k in range(len(contacts[j]["Address"])):
                if tempnum==contacts[j]["Address"][k]:
                    if contacts[j]["Last"] != None:
                        tempname=contacts[j]["First"]+u' '+contacts[j]["Last"]
                    elif contacts[j]["Last"] == None:
                        tempname=contacts[j]["First"]
                elif tempnum==None:
                    tempname=None
        if sms[i][4]==3:
            sr="Sent"
        elif sms[i][4]==2:
            sr="Received"
        date=str(sms[i][2])
        dt=datetime.fromtimestamp(int(date))
        ds=dt.strftime("%Y-%m-%d %H:%M:%S")
        date=ds.decode('utf-8')


        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:10])
        hour=int(date[11:13])
        minute=int(date[14:16])
        sec=int(date[17:19])

        datedt=todatenum(datetime(year,month,day,hour,minute,sec))

        
        try:
            tempdict={"Text":sms[i][3],"Date":date,"Contact":tempname,"Address":tempnum,"sr":sr,"Datetime":datedt}
        except:
             tempdict={"Text":sms[i][3],"Date":date,"Contact":None,"Address":sms[i][1],"sr":sr,"Datetime":datedt}

        sms_database.append(tempdict)
########
    elif sms[i][4]==0 and sms[i][29]!=22 and sms[i][26]!=32773:
        tempnum=sms[i][18]
        try:
            tempnum=re.sub("[^0-9]","",tempnum)
            if tempnum[0] != u'1':
                tempnum=u'1'+tempnum
            tempnum=u'+'+tempnum
        except:
            pass

        for j in range(len(contacts)):
            for k in range(len(contacts[j]["Address"])):
                if tempnum==contacts[j]["Address"][k]:
                    if contacts[j]["Last"] != None:
                        tempname=contacts[j]["First"]+u' '+contacts[j]["Last"]
                    elif contacts[j]["Last"] == None:
                        tempname=contacts[j]["First"]
                elif tempnum==None:
                    tempname=None
        if sms[i][26]==36869 or sms[i][26]==102405:
            sr="Sent"
        elif sms[i][26]==12289 or sms[i][26]==77825:
            sr="Received"
        if sms[i][31]==0:
            date=str(int(sms[i][32]+978307200))
        else:
            date=str(int(sms[i][31]+978307200))
        dt=datetime.fromtimestamp(int(date))
        ds=dt.strftime("%Y-%m-%d %H:%M:%S")
        date=ds.decode('utf-8')


        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:10])
        hour=int(date[11:13])
        minute=int(date[14:16])
        sec=int(date[17:19])

        datedt=todatenum(datetime(year,month,day,hour,minute,sec))

        try:
            tempdict={"Text":sms[i][3],"Date":date,"Contact":tempname,"Address":tempnum,"sr":sr,"Datetime":datedt}
        except:
            tempdict={"Text":sms[i][3],"Date":date,"Contact":None,"Address":sms[i][1],"sr":sr,"Datetime":datedt}

        sms_database.append(tempdict)

#######


if databaseq=='y':
    newtime=0
    for i in range(len(smsdb)):
        temptime=smsdb[i]["Datetime"]
        if temptime>newtime:
            newtime=temptime

    for i in range(len(sms_database)):
        if sms_database[i]["Datetime"]>newtime:
            smsdb.append(sms_database[i])

    smsdb=smsclass(smsdb)
    

if databaseq=='n':
    smsdb=smsclass(sms_database)
q4=raw_input("Would you like to pickle this database for future use? (y/n):  ")
if q4 == 'y':      
    q2=raw_input("Enter the location where you would like the database file pickled:\n")
    pickle.dump(smsdb,open(q2,'wb'))

print("\nAlright! You're all done! The variable *smsdb* is the database. You can \
now perform some neat little functions on it. They are all listed in sms.py. You \
can used them by doing: smsdb.function()\nAn example would be to try: smsdb.total()")

