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




def todatenum(d):
    # d is a datetime.datetime or a datetime.time object
    try: d1=d.toordinal()
    except: d1=0
    d2=(d.hour+(d.minute+d.second/60.)/60.)/24.
    dn=d1+d2
    return dn

try:
    smsdb=pickle.load(open("sms_database.p","rb"))
    database='y'
except:
    database='n'

os.system("cp /Users/"+getuser()+"/Library/Application\ Support/MobileSync/Backup/3a09e92209b9e3cd0520ef7ecd4373bb55db1c2d/3d0d7e5fb2ce288813306e4d4636395e047a3d28 /Users/landan/Documents/Texts_from_orrin/sms.db")
smsDB = sqlite3.connect('sms.db')
with smsDB:
    cur = smsDB.cursor()
    cur.execute("SELECT * FROM message")

    sms = cur. fetchall()

sms_orrin=[]
for i in range(len(sms)):
    if sms[i][1]==u'+19028800158' or sms[i][1]==u'+15064800006':
        sms_orrin.append(sms[i])
orrin=[]

for i in range(len(sms_orrin)):
    if sms_orrin[i][4]==3:
        sentby='Landan'
    elif sms_orrin[i][4]==2:
        sentby='Orrin'
    text=sms_orrin[i][3]
    date=str(sms_orrin[i][2])
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

    tempdict={"date":str(date),"datetime":datedt,"Sent By":sentby,"text":text}
    orrin.append(tempdict)

times=[]
for i in range(len(orrin)):
    times.append(orrin[i]["datetime"])
if database=='y':
    newtime=0
    for i in range(len(smsdb)):
        temptime=smsdb[i]["datetime"]
        if temptime>newtime:
            newtime=temptime

    for i in range(len(orrin)):
        if orrin[i]["datetime"]>newtime:
            smsdb.append(orrin[i])

    smsdb=smsclass(smsdb)
    pickle.dump(smsdb,open("/Users/landan/Documents/Texts_from_orrin/sms_database.p",'wb'))

if database=='n':
    pickle.dump(orrin,open("/Users/landan/Documents/Texts_from_orrin/sms_database.p",'wb'))


