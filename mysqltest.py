import MySQLdb
import time
import datetime
import csv

now=time.time()
db = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="wd5158108",db="qickd2" )
c=db.cursor()
c.execute("SELECT distinct id FROM qickd2.journalsubset where code like 'eGFRorig'")
ID=c.fetchall()
ids=[]
for i in ID:
    ids.append(i[0])
ids.sort(reverse=False)
print ids[4]
print len(ids)
filename=open('csvfile2.csv','wb')
field=['ID','start date','end date','variation']
csvfile=csv.writer(filename)
csvfile.writerow(field)
##ids=[89732,1090880]
##lists=[]
count=0
tmp=datetime.date
for i in ids:
##    if i <2403608:
##        break
    count+=1
    c.execute ("SELECT * FROM qickd2.journalsubset where code like 'eGFRorig' and id like '{}'".format(i)) 
    person=c.fetchall()
    tmp=person[0][2]
    for j in range(len(person)):
        
        for k in range(j,len(person)):
            if ((person[k][2]-person[j][2])>datetime.timedelta(days=182))and (tmp< person[k-1][2]) and ((person[k-1][2]-person[j][2])<datetime.timedelta(days=182)) and (person[k-1][2]!=person[j][2]) and(person[j][2]>=tmp):
               csvfile.writerow([person[j][0],person[j][2],person[k-1][2],person[k-1][3]-person[j][3]])
               tmp=person[k-1][2]
               break
    if count%1000==0 :
        print time.time()-now,'s past, id is: ',i
filename.close()
    
    
##for i in ids:
##    c.execute ("SELECT * FROM qickd2.journalsubset where code like 'eGFRorig' and id like '{}'".format(i)) 
##    person=c.fetchall()
##    print person
