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

##
