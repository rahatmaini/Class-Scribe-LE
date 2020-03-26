import unittest
import main
import returnIDnumbers as retIDs
import os
import picamera
import textIP
import transcribe
import getRoomAssignments
import capture 

class TestStringMethods(unittest.TestCase):

    def test_successful_ID_retrieval(self):
	    self.assertTrue(retIDs.findIfIDnumberPresent("21526833781"))
    
    def test_ID_input(self):
        self.assertEqual("1",main.waitingForID())

    def test_successful_ID_rejection(self):
	    self.assertFalse(retIDs.findIfIDnumberPresent("2153443218")) #Ben's ID is not in the database

    def test_audio_recorded(self):
	#    os.system("arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav")
        capture.audioRecord("test.wav")
        self.assertTrue(os.path.exists("test.wav"))
    
    def test_image_capture(self):
	    camera=picamera.PiCamera()
	    camera.capture("test.jpg")
	    self.assertTrue(os.path.exists("test.jpg"))

    def test_text_IP(self):
        self.assertTrue(main.printOutIP()) # if error, will return false
    
    def test_transcription_file_decoder(self):
        self.assertEqual("how old is the Brooklyn Bridge",transcribe.transcribe())

    def test_get_email_and_pk_by_id(self):
        idNumber = "2152683378"
        self.assertEqual(("rm4mp@virginia.edu",22),retIDs.getEmailAddressAndPK(idNumber))

    def test_getting_classname(self):
        # testing the first dummy course, whether it is returned properly or not
        self.assertEqual(getRoomAssignments.getClassName(),"course1")
    
    def test_getting_timeIncluded_edge_cases(self):
        os.system('sudo date -s "26 MAR 2020 09:00:00"')
        self.assertTrue(getRoomAssignments.isTimeIncluded("MTuWThuF 8:45-10:00"))

    def test_getting_timeExcluded(self):
        os.system('sudo date -s "28 MAR 2020 00:20:50"')
        self.assertFalse(getRoomAssignments.isTimeIncluded("MTuWThuF 8:45-10:00"))
    
    def test_dependent_on_user_input(self):
        self.assertTrue(main.mainLoop())  # for this test to pass, must enter an ID number in the system such as 2153443218
    
    def test_no_ID_in_system_so_add_one(self):
        self.assertFalse(main.mainLoop()) # for this test to pass, enter an ID number then input it into Django admin (as the linkage of ID/student happens off the Pi, untestable here)
    
    def test_capture(self):
        self.assertTrue(capture.capture("course1","rm4mp@virginia.edu",22))
if __name__ == '__main__':
    unittest.main()
