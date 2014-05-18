import MySQLdb
import time
import datetime
import csv

usr = 'root'
pwd = '1234'

now=time.time()
db = MySQLdb.connect(host="127.0.0.1",port=3306,user=usr,passwd=pwd,db="qickd2" )
c=db.cursor()
c.execute("SELECT distinct code FROM qickd2.codinggroup where value1min = -99.00")
code1=[x[0] for x in c.fetchall()]
c.execute("SELECT distinct code FROM qickd2.codinggroup where value1min != -99.00")
code2=[x[0] for x in c.fetchall()]
print type(code1[0])
print len(code2)

file1 = open('sample.csv','rb')
csv_file = csv.DictReader(file1, delimiter=',',quotechar='"')
currentID = '000000'
currentcode = []
file1 = open('data__.txt','w')


for i in csv_file:
    if not (i['ID'].startswith(currentID)):
        file1.flush()
        currentID = i['ID']
        c.execute ("SELECT * FROM qickd2.journalsubset WHERE code not like 'eGFRorig' and id like '{}'".format(currentID))
        currentcode = list(c.fetchall())
    if len(currentcode)==0:
        continue
    file1.write(i['ID']+':'+i['start_date']+',,,'+i['variation']+':')
    valued_code={}
    for code in currentcode:
        if str(code[2]) >= i['start_date'] and str(code[2]) <= i['end_date']:
            if code[3] == 0.00:
##                file1.write(code[1]+' ')
                for prefix in code1:
                    if code[1].startswith(prefix):
                        file1.write(prefix+' ')
                        break
            else:
##                if valued_code.has_key(code[1]):
##                    valued_code[code[1]].append([code[2],code[3]])
##                else:
##                    valued_code.update({code[1]:[[code[2],code[3]]]})
                for prefix in code2:
                    if code[1].startswith(prefix):
                        if valued_code.has_key(prefix):
                            valued_code[prefix].append([code[2],code[3]])
                        else:
                            valued_code.update({prefix:[[code[2],code[3]]]})
                        break
            currentcode.remove(code)
##        else:
##            print str(code[2])+': '+i['start_date']+' - '+i['end_date']
    for prefix in valued_code.keys():
        if len(valued_code[prefix]) <= 1:
            continue
        else:
            max_val = valued_code[prefix][0]
            min_val = valued_code[prefix][0]
            for val in valued_code[prefix]:
                if max_val[0] < val[0]:
                    max_val = val
                if min_val[0] > val[0]:
                    min_val = val
            if max_val[1] - min_val[1] > 0:
                file1.write(prefix+'_up ')
            else:
                file1.write(prefix+'_down ')

    file1.write('\n')
    print currentID+ ': '+str(len(currentcode))
file1.close()
