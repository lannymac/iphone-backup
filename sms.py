#! /usr/bin/python

'''
This program will be used to read in sms messages and 
save them into an array for database purposes. Will Probably
pickle them. Might even make an sms class
'''


import sms

class sms(list):

    def name(self,i):
        '''Prints the name of who sent message # i'''
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


    def daytext(self,contact=0):            
        '''This will print all texts from a certain date entered'''

        from datetime import datetime
        import copy
        date=raw_input("Enter the date you would like to see the texts (format yyyy,mm,dd):  ")
        #change the date entered into datetime format
        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:10])
        datedt=datetime(year,month,day,0,0,0)
        finaldate=datedt.toordinal()

        #Go through the entire database or just search through for a certain contact
        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name="all contacts"
        #go through entire database
        for i in range(len(database)):
            if int(database[i]["Datetime"])==finaldate: #check to make sure that the days match up
                if database[i]["sr"]=='Received':#check if received, then print to the screen
                    print("Sent by: "+database[i]["Contact"]+", Received by: you at "+str(database[i]["Date"][11:])+"\n")
                    print(database[i]["Text"])
                    print("\n")
                    print("------")
                    print("\n")
                if database[i]["sr"]=='Sent':#check if sent, then print to the screen
                    print("Sent by: you, Received by: "+database[i]["Contact"]+" at "+str(database[i]["Date"][11:])+"\n")
                    print(database[i]["Text"])
                    print("\n")
                    print("------")
                    print("\n")
                
    
    def total(self,contact=0):        
        from matplotlib import dates
        import pylab as pl
        from collections import Counter
        import copy
        from sms import findcontact

        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name="all contacts"
                                  

        time=[]
        count=[]
        for i in range(len(database)):
            time.append(int(database[i]["Datetime"]))

        timedict=Counter(time)
        time=list(timedict)
        for i in time:
            count.append(timedict[i])
        dates = dates.num2date(time)
        fig=pl.figure()
        ax=fig.add_subplot(111)
        
        ax.bar(dates,count,linewidth=0.1,color='r')
        ax.autoscale_view()
        ax.grid(True)
        pl.xlabel("Date")
        pl.ylabel("Messages per day")
        fig.autofmt_xdate()
        pl.title('Texts sent from '+name)
        pl.show()
        
    def srplot(self,contact=0):
        from matplotlib import dates
        from collections import Counter
        import copy
        import pylab as pl

        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name='all contacts'

        senttime=[]
        sentcount=[]
        rectime=[]
        reccount=[]

        for i in range(1,len(database)):
            if database[i]["sr"]=="Sent":
                senttime.append(int(database[i]["Datetime"]))
            if database[i]["sr"]=="Received":
                rectime.append(int(database[i]["Datetime"]))

        senttimedict=Counter(senttime)
        rectimedict=Counter(rectime)
        senttimedict=sorted(senttimedict.items())
        rectimedict=sorted(rectimedict.items())

        senttime=[]
        sentcount=[]
        rectime=[]
        reccount=[]
        for i in range(len(senttimedict)):
            senttime.append(senttimedict[i][0])
            sentcount.append(senttimedict[i][1])
        for i in range(len(rectimedict)):
            rectime.append(rectimedict[i][0])
            reccount.append(rectimedict[i][1])



        datesent = dates.num2date(senttime)
        daterec = dates.num2date(rectime)
        fig=pl.figure()
        ax=fig.add_subplot(111)
        
        ax.plot(datesent,sentcount,color='c',label="Sent")
        ax.autoscale_view()
        ax.grid(True)

        pl.ylabel("Messages per day")
        fig.autofmt_xdate()
        ax.plot(daterec,reccount,color='m',label="Recieved")
        ax.autoscale_view()
        ax.grid(True)
        pl.legend()
        pl.title('Texts sent from '+name)
        pl.show()


    def sr(self,contact=0):
        import pylab as pl
        from collections import Counter
        import copy
        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name='all contacts'

        time=[]
        count=[]
        for i in range(1,len(database)):
            time.append(int(database[i]["Datetime"]))
        timedict=Counter(time)
        time=list(timedict)
        senttime=[]
        sentcount=[]
        rectime=[]
        reccount=[]

        for i in range(1,len(database)):
            if database[i]["sr"]=="Sent":
                senttime.append(int(database[i]["Datetime"]))
            if database[i]["sr"]=="Received":
                rectime.append(int(database[i]["Datetime"]))

        senttimedict=Counter(senttime)
        rectimedict=Counter(rectime)
        senttime=list(senttimedict)
        rectime=list(rectimedict)
        for i in senttime:
            sentcount.append(senttimedict[i])
        for i in rectime:
            reccount.append(rectimedict[i])
        print("Data from "+name)
        print("Total texts SENT over "+str(max(time)-min(time))+" days: "+str(sum(sentcount)))
        print("Average texts SENT per day: "+str(round(sum(sentcount)/float(len(sentcount)),2)))
        print("\n")
        print("Total texts RECEIVED over "+str(max(time)-min(time))+" days: "+str(sum(reccount)))
        print("Average texts RECEIVED per day: "+str(round(sum(reccount)/float(len(reccount)),2)))

    def dayplot(self,contact=0):
        import pylab as pl
        from collections import Counter
        import copy
        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name='all contacts'
        
        hours=range(0,24)
        hourcount=[]
        for i in range(len(hours)):
            hourcount.append(0)

        for i in range(1,len(database)):
            temphour=int(database[i]["Date"][11:13])
            hourcount[temphour]=hourcount[temphour]+1
        
        total_mess=sum(hourcount)
        for i in range(len(hourcount)):
            hourcount[i]=hourcount[i]/float(total_mess)
        

        pl.figure()
        pl.bar(hours,hourcount)
        #pl.plot(hours,hourcount,'.',linewidth=2)
        pl.xlabel("Hour of the day")
        pl.ylabel("Fraction of total texts")
        pl.xlim(0,24)
        pl.title("Texts sent from "+name)
        pl.axis('tight')
        pl.show()
    def monthplot(self,contact=0):
        import pylab as pl
        import copy
        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name='all contacts'
        months=range(1,13)
        monthcount=[]
        for i in range(len(months)):
            monthcount.append(0)

        for i in range(1,len(database)):
            tempmonth=int(database[i]["Date"][5:7])
            monthcount[tempmonth-1]=monthcount[tempmonth-1]+1

        total_mess=sum(monthcount)
        for i in range(len(monthcount)):
            monthcount[i]=monthcount[i]/float(total_mess)

        pl.figure()
        pl.bar(months,monthcount)
        #pl.plot(hours,hourcount,'.',linewidth=2)
        pl.xlabel("Month #")
        pl.ylabel("Fraction of total texts")
        pl.xlim(0,24)
        pl.title('Texts sent from '+name)
        pl.axis('tight')
        pl.show()


    def wordfreq(self,word,contact=0):

        import copy
        import pylab as pl
        from collections import Counter
        from matplotlib import dates
        import copy
        if contact!=0:
            database,name=findcontact(self)
        else:
            database=copy.deepcopy(self[1:])
            name='all contacts'

        word=word.lower()
        if len(word)>0:
            daycount=[]
            count=[]
            for i in range(len(database)):
                findnum=0
                day=int(database[i]["Datetime"])
                string=copy.deepcopy(database[i]["Text"])
                

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
            daydict=sorted(daydict.items())

            day=[]
            count=[]
            for i in range(len(daydict)):
                day.append(daydict[i][0])
                count.append(daydict[i][1])
            dateplot=dates.num2date(day)
            fig=pl.figure()
            ax=fig.add_subplot(111)
            ax.plot(dateplot,count)
            ax.autoscale_view()
            ax.grid(True)
            fig.autofmt_xdate()

            pl.title('Frequency of the word '+word.upper()+' sent from '+name)
            pl.ylabel('Word frequency [word/day]')
            pl.show()
            print("Average frequency of the word "+word.upper()+" used per day: "+str(round(sum(count)/float(database[-1]["Datetime"]-database[0]["Datetime"]),2)))
    def export(self,contact=0):
        import codecs
        import copy
        where=raw_input("Where would you like the exported file saved?  ")

        if contact!=0:
            database,name=findcontact(self)
            name=name.replace(' ','_')
        else:
            database=copy.deepcopy(self[1:])
            name='all_contacts'

        f=codecs.open(where+"sms_"+name+".txt","w","utf-8")

        for i in range(len(database)):
            contact=database[i]["Contact"]
            if contact==None:
                if database[i]["Address"]!=None:
                    contact=database[i]["Address"]
                else:
                    contact="No one"
      
            if database[i]["sr"]=="Sent":
                f.write("Sent by: YOU, Received by: "+contact+" on "+str(database[i]["Date"])+"\n")
                f.write("\n")
                if database[i]["Text"]!=None:
                    f.write(database[i]["Text"])
                f.write("\n")
                f.write("----------")
                f.write("\n")
            else:
                f.write("Sent by: "+contact+", Received by: YOU"+" on "+str(database[i]["Date"])+"\n")
                f.write("\n")
                if database[i]["Text"]!=None:
                    f.write(database[i]["Text"])
                f.write("\n")
                f.write("----------")
                f.write("\n")
            


def findcontact(self):
    from collections import Counter
    import copy
    contacts=[]
    print("Here is a list of your contacts. Enter the number corresponding to the contact you wish to isolate:  ")
    for i in range(len(self[0])):
        if self[0][i]["First"]!=None and self[0][i]["Last"]!=None:
            print(str(i)+" - "+self[0][i]["First"]+" "+self[0][i]["Last"])
            contacts.append(self[0][i]["First"]+" "+self[0][i]["Last"])
        elif self[0][i]["First"]==None and self[0][i]["Last"]!=None:
            print(str(i)+" - "+self[0][i]["Last"])
            contacts.append(self[0][i]["Last"])
        elif self[0][i]["First"]!=None and self[0][i]["Last"]==None:
            print(str(i)+" - "+self[0][i]["First"])
            contacts.append(self[0][i]["First"])
        else:
            print(str(i)+" - "+"No contact Name")
            contacts.append("No contact name")
    q=raw_input("Enter a number:  ")
    print("Showing texts for only "+contacts[int(q)])
    database=[]
    for i in range(1,len(self)):
        try:
            if self[i]["Contact"]==contacts[int(q)]:
                database.append(copy.deepcopy(self[i]))
        except:
            pass    
    return database,contacts[int(q)]
