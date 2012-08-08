#! /usr/bin/python

'''
This program will be used to read in sms messages and 
save them into an array for database purposes. Will Probably
pickle them. Might even make an sms class
'''


import sms

class sms(list):

    def name(self,i):
        print(self[i]["Contact"])

    def text(self,i):
        print(self[i]["Text"])

    def date(self,i):
        print(self[i]["Date"])
        
    def sr(self,i):
        print(self[i]["sr"])

    def dt(self,i):
        print(self[i]["Datetime"])

    def all(self,i):
        if self[i]["sr"]=="Sent":
            print("Seny by: YOU"+"\n"+"Received by: "+str(self[i]["Contact"])+" on "+str(self[i]["Date"])+"\n")
            print(self[i]["Text"])

        elif self[i]["sr"]=="Received":
            print("Seny by: "+str(self[i]["Contact"])+"\n"+"Received by: YOU"+" on "+str(self[i]["Date"])+"\n")
            print(self[i]["Text"])

    def daytext(self):
        from datetime import datetime
        date=raw_input("Enter the date you would like to see the texts (format yyyy,mm,dd):  ")
        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:10])
        datedt=datetime(year,month,day,0,0,0)
        finaldate=datedt.toordinal()
        
        for i in range(len(self)):
            if int(self[i]["datetime"])==finaldate:
                print("Seny by: "+self[i]["Sent By"]+" at "+str(self[i]["date"][11:])+"\n")
                print(self[i]["text"])
                print("\n")
                print("------")
                print("\n")
                
             
    
    def total(self):

        import pylab as pl
        from collections import Counter
        time=[]
        count=[]
        for i in range(len(self)):
            time.append(int(self[i]["Datetime"]))

        timedict=Counter(time)
        time=list(timedict)
        for i in time:
            count.append(timedict[i])
        
        pl.figure()
        pl.bar(time,count,color='r',label="TOTAL")
        pl.ylabel("Number of Messages")
        pl.show()
        
    def srplot(self):
        from collections import Counter
        import pylab as pl
        senttime=[]
        sentcount=[]
        rectime=[]
        reccount=[]

        for i in range(len(self)):
            if self[i]["sr"]=="Sent":
                senttime.append(int(self[i]["Datetime"]))
            if self[i]["sr"]=="Received":
                rectime.append(int(self[i]["Datetime"]))

        senttimedict=Counter(senttime)
        rectimedict=Counter(rectime)
        senttime=list(senttimedict)
        rectime=list(rectimedict)
        for i in senttime:
            sentcount.append(senttimedict[i])
        for i in rectime:
            reccount.append(rectimedict[i])

        pl.figure()
        pl.plot(senttime,sentcount,'b-',label="Sent")
        pl.plot(rectime,reccount,'g-',label="Received")
        pl.xlabel("Time")
        pl.ylabel("Messages per day")
        pl.legend()
        pl.show()

    def sr(self):
        import pylab as pl
        from collections import Counter
        time=[]
        count=[]
        for i in range(len(self)):
            time.append(int(self[i]["Datetime"]))
        timedict=Counter(time)
        time=list(timedict)
        senttime=[]
        sentcount=[]
        rectime=[]
        reccount=[]

        for i in range(len(self)):
            if self[i]["sr"]=="Sent":
                senttime.append(int(self[i]["Datetime"]))
            if self[i]["sr"]=="Received":
                rectime.append(int(self[i]["Datetime"]))

        senttimedict=Counter(senttime)
        rectimedict=Counter(rectime)
        senttime=list(senttimedict)
        rectime=list(rectimedict)
        for i in senttime:
            sentcount.append(senttimedict[i])
        for i in rectime:
            reccount.append(rectimedict[i])
        print("Total texts SENT over "+str(max(time)-min(time))+" days: "+str(sum(sentcount)))
        print("Average texts SENT per day: "+str(round(sum(sentcount)/float(len(sentcount)),2)))
        print("\n")
        print("Total texts RECEIVED over "+str(max(time)-min(time))+" days: "+str(sum(reccount)))
        print("Average texts RECEIVED per day: "+str(round(sum(reccount)/float(len(reccount)),2)))

    def dayplot(self):
        import pylab as pl
        hours=range(0,24)
        hourcount=[]
        for i in range(len(hours)):
            hourcount.append(0)

        for i in range(len(self)):
            temphour=int(self[i]["Date"][11:13])
            hourcount[temphour]=hourcount[temphour]+1


        pl.figure()
        pl.bar(hours,hourcount)
        #pl.plot(hours,hourcount,'.',linewidth=2)
        pl.xlabel("Hour of the day")
        pl.ylabel("Sum of texts")
        pl.xlim(0,24)
        pl.axis('tight')
        pl.show()
    def monthplot(self):
        import pylab as pl
        months=range(1,13)
        monthcount=[]
        for i in range(len(months)):
            monthcount.append(0)

        for i in range(len(self)):
            tempmonth=int(self[i]["Date"][5:7])
            monthcount[tempmonth-1]=monthcount[tempmonth-1]+1


        pl.figure()
        pl.bar(months,monthcount)
        #pl.plot(hours,hourcount,'.',linewidth=2)
        pl.xlabel("Month #")
        pl.ylabel("Sum of texts")
        pl.xlim(0,24)
        pl.axis('tight')
        pl.show()


    def wordfreq(self,word):

        import copy
        import pylab as pl
        from collections import Counter
        word=word.lower()
        if len(word)>0:
            daycount=[]
            count=[]
            for i in range(len(self)):
                findnum=0
                day=int(self[i]["Datetime"])
                string=copy.deepcopy(self[i]["Text"])
                

                while 1:
                    if string==None:
                        break
                    string=string.lower()
                    findnum = string.find(word)

                    if findnum == -1:
                        break
                    string=string[findnum+1:]
                    daycount.append(day)

            daydict=Counter(daycount)
            day=list(daydict)
            for i in day:
                count.append(daydict[i])


            print("Average frequency of the word "+word.upper()+" used per day: "+str(round(sum(count)/float(self[-1]["Datetime"]-self[0]["Datetime"]),2)))
            pl.figure()
            pl.plot(day,count)
            pl.show()

    def export(self):
        where=raw_input("Where would you like the exported file saved?  ")
        f=open(where+"smsoutput.txt","w")
        for i in range(len(self)):
            try:
                f.write("Sent by: "+self[i]["Sent By"]+" on "+str(self[i]["date"])+"\n")
                f.write("\n")
                f.write(str(self[i]["text"]))
                f.write("\n")
                f.write(str(i))
                f.write("----------")
                f.write("\n")
            except:

                pass

