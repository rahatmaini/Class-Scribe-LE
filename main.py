import time
import inkyphat
from PIL import Image, ImageFont, ImageDraw
import subprocess
import requests
import picamera
import datetime
import os

import textIP
import capture
import getRoomAssignments
#import qr
import returnIDnumbers

inkyphat.set_colour("black")
font = ImageFont.truetype(inkyphat.fonts.AmaticSCBold, 38)


#def printWelcomeMsg():
 #   img = Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
  #  draw = ImageDraw.Draw(img)
#
 #   message = "Welcome"
#
 #   w, h = font.getsize(message)
  #  x = (inkyphat.WIDTH / 2) - (w / 2)
   # y = (inkyphat.HEIGHT / 2) - (h / 2)
#
 #   draw.text((x, y), message, inkyphat.BLACK, font)
  #  inkyphat.set_image(img)
   # inkyphat.show()

def waitingForID(): #loop till ID is presented
	flag = 1
	while (flag):
		idNumber=raw_input()
		flag = 0
	return idNumber

def printOutIP(): #for debugging, prints out wlan0 IP of Pi to screen
    out = subprocess.Popen(['hostname', '-I'],
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)


    #img = Image.new("P", (inkyphat.WIDTH, inkyphat.HEIGHT))
    #draw = ImageDraw.Draw(img)

    message = str(out.communicate()[0])
    textIP.textIPtoRahat(message)

    #w, h = font.getsize(message)
    #x = (inkyphat.WIDTH / 2) - (w / 2)
    #y = (inkyphat.HEIGHT / 2) - (h / 2)

    #draw.text((x, y), message, inkyphat.BLACK, font)
    #inkyphat.set_image(img)
    #inkyphat.show()
    return True

def mainLoop():
    idNumber=waitingForID() #read encrypted version of the ID number
    print ("ID number: ", idNumber)

    if (returnIDnumbers.findIfIDnumberPresent(idNumber)):
        print ("ID is in database")
        className=getRoomAssignments.getClassName()
        emailAddressAndPK=returnIDnumbers.getEmailAddressAndPK(idNumber)
        print ("Email address and PK:", emailAddressAndPK)


        if (className != 0):
            print ("Class name: ", className)
                # capture.capture(className,emailAddressAndPK[0],emailAddressAndPK[1]) requires specialized hardware unable for testing remotely, these components will be tested individually
            return True

    else: #not in database, generate QR code to assign encrypted ID to a user
           # qr.printQRcode(idNumber) not using this in hardware revision 2
        print ("id is not in database")
        flag = 1
        while (flag):
            if (returnIDnumbers.findIfIDnumberPresent(idNumber)):
                className=getRoomAssignments.getClassName()
                emailAddressAndPK=returnIDnumbers.getEmailAddressAndPK(idNumber)
                flag=0
                break
            time.sleep(3.5)
           # printWelcomeMsg()
        if (className != 0):
                # capture.capture(className,emailAddressAndPK[0],emailAddressAndPK[1]) see above for why commented out during testing, unable to proceed if enabled
            return False

# code commented for testing, no logic only control flow essential to actual physical use rather than testing
#if __name__ == '__main__':
    #os.system("sudo ntpdate us.pool.ntp.org")
    #printOutIP()
 #   while (1):
        #printWelcomeMsg()  
  #      mainLoop()      
        
