import json
import urllib2


def findIfIDnumberPresent(idNumber):

    url = "http://128.143.67.97:44104/IDexists/articles/" + idNumber + "?format=json"
    response = urllib2.urlopen(url)

    data = json.loads(response.read())

    return (idNumber in str(data))

def getEmailAddressAndPK(idNumber):
    url = "http://128.143.67.97:44104/api/getUserEmailAndPKByID/" + idNumber + "?format=json"
    response = urllib2.urlopen(url)

    data = json.loads(response.read())
    
    return (str(data["email"]),data["pk"])

