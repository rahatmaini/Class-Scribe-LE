import json
import urllib2
import datetime


lampSerialNumber="0123456789abcdef"

def isTimeIncluded(assignmentTime):
    dayOfWeek=datetime.datetime.today().weekday()
    currentTime=str(datetime.datetime.now().time().hour)
    if ((datetime.datetime.now().time().minute))<10:
        currentTime+="0"+(str(datetime.datetime.now().time().minute))
    else:
        currentTime=int(str(datetime.datetime.now().time().hour)+(str(datetime.datetime.now().time().minute)))
    currentTime = int(currentTime)
    daysOfWeek={ "M":0, "Tu":1, "W":2, "Th":3, "F":4 }
    
    assignmentDays=[]

    for k in daysOfWeek.keys():
        if k in assignmentTime:
            assignmentDays.append(daysOfWeek[k])

    assignmentTime=str(assignmentTime[assignmentTime.find(" ")+1:]).replace(":","")
    assignmentTime=(int(assignmentTime[0:assignmentTime.find("-")]),int(assignmentTime[assignmentTime.find("-")+1:]))
    
    if (dayOfWeek in assignmentDays and currentTime>= assignmentTime[0] and currentTime <= assignmentTime[1]):
        print (dayOfWeek, assignmentDays, currentTime, assignmentTime)
        return True
    else:
        return False



def getClassName():

    url = "http://128.143.67.97:44104/courses/getAdminAssignments/?format=json"
    response = urllib2.urlopen(url)

    data = json.loads(response.read()).get("assignments")

    for i in data:
        print
        if str(i.get("lamp_serial"))==lampSerialNumber and isTimeIncluded(i.get("time")) and str(i.get("semester"))=="Spring 2020":
            return (i.get("name"))
    #print ("getRoomAssignments.py data:", data)
    return 0


