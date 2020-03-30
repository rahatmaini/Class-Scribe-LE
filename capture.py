import subprocess
import time
import threading
import requests
import datetime
import transcribe
import apiCalls
import os

imageTimeStamps=[]
counter = 0

def audioRecord(filename):
	test2 = subprocess.Popen(["arecord", "--device=hw:1,0", "--format", "S16_LE", "--rate", "44100", "--duration=50", filename+".wav"], stdout=subprocess.PIPE)
	output2 = test2.communicate()[0]

def newPageInput():
    while (1):
        test3 = input()

def takePhotos(filename):
    t0 = time.time()
    flag = 1
    global counter 
    while (flag):
        test = subprocess.Popen(["raspistill","-o",str(filename+str(counter))+".jpg"], stdout=subprocess.PIPE)
        imageTimeStamps.append(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        output = test.communicate()[0]
        currTime = int(str(datetime.datetime.now().time().hour)+str(datetime.datetime.now().time().minute))
        counter+=1
        if (time.time() - t0 >= 50):   #DURATION!!
            flag = 0
            break

def capture(className, email, pk):
    timeStampedFileName=str(time.time()).replace(".","")

    t1 = threading.Thread(target=audioRecord, args=(timeStampedFileName,))
    t2 = threading.Thread(target=takePhotos, args=(timeStampedFileName,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    uploadFiles(timeStampedFileName, className, email, pk)

def uploadFiles(filename, className, email, pk):
    
    audioPK=apiCalls.uploadAudio(filename+".wav", email, className, "5", str(time.time()))
    #counter is number of photos-1
    print ("audio pk:", audioPK)
    notebookPK = apiCalls.createNotebook(False, className, email+"'s "+className, pk)
    print ("notebookPK", notebookPK)
    print (counter)
    x = 0
    imagesPK=[]
    pagesPK=[]
    while (x<counter):
        if (os.path.isfile(filename+str(x)+".jpg")):
            print (x)
            imagesPK.append(int(apiCalls.createImage(filename+str(x)+".jpg",email, className, "1", imageTimeStamps[x])))
        x+=1

    pagesPK.append(apiCalls.createPage(str(datetime.datetime.now()).split()[0],str(datetime.datetime.now()),notebookPK))
    for item in imagesPK:
        apiCalls.addImagestoPage(int(pagesPK[0]), item, email, className)
    print (imagesPK[0],imagesPK[-1])
    #at this point, uploaded audio and uploaded images
        
    transcript='something'
    
    try:
        os.system("gcloud ml speech recognize "+ filename+".wav " + "--language-code='en-US' > test.json")
        os.system("gcloud ml speech recognize "+ filename+".wav " + "--language-code='en-US' > test.json")
        transcript=transcribe.transcribe()
    except Exception as e:
        print (e)
        transcript="RESOURCE_EXHAUSTED: Daily upload quota for class.scribe.co@gmail.com exceeded."

    apiCalls.addAudioAndTranscription(audioPK,int(pagesPK[0]), transcript)

     
    



