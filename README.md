# Class-Scribe-LE
Lamp Scripts to interface with Class Scribe backend   
  
## main.py  
The main code that is run and calls all other code  
  
Responsible for:  
- Reading ID numbers from RFID chip  
- Interfacing with E-Paper display (in hardware version 1)  
- Setting proper time/date for Lamp  
- Sequentially running Lamp workflow 

Sequence of actions:  
1. Wait for ID to be scanned  
2. Check if ID number exists in Class Scribe database
3. If not, produce QR code for user to scan and register themselves  
4. If yes or as soon as registered, retrieve room assignment based on current time
5. Retrieve student email adress  
6. Begin capturing images/audio, assigned to a user email, under retrieved course name, and then send notebook to backend  

## apiCalls.py  
All requests to be sent from the Lamp to the Class Scribe backend  

## capture.py  
The code that captures images and records audio. Multithreaded to allow for simultaneous record/capture. Also responsible for calling apiCalls.py to upload captured data to backend. Finally, capture.py is also responsible for transcription (this should be fixed and done in a different file for clarity)  

## getRoomAssignments.py  
This code is where the serial number for the Lamp is defined.

- Checks if the current time and date match up with a time and date for a class session occuring, in the database.  
- If there is a current session occuring, returns the name of the class occuring, to be used for notebook identification/creation.  

## qr.py
In hardware version 1, each Lamp does not have a static QR code unique to it. Instead it generates a QR code with an ID number encoded into it. This code does so, once main.py receives an ID number and calls it.  

NOTE: The next revision of the Lamp has a static QR code that uniquely identifies the Lamp. Once scanned, the backend will serve up the most recently scanned ID by THAT Lamp automatically for ID/Student linkage. This is how we make static QR codes work (saves money, power consumption, system resources, and better for aesthetics than having a display fixed to the Lamp).  

## returnIDnumbers.py  
This code provides two helper functions: one to check if an ID number exists in the Class Scribe database, and one to retrieve an email address and primary key for a student in the Class Scribe database based on their ID number.
