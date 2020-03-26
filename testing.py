import unittest
import main
import returnIDnumbers as retIDs
import os
import picamera
import textIP
import transcribe
import getRoomAssignments

class TestStringMethods(unittest.TestCase):

    def test_successful_ID_retrieval(self):
	    self.assertTrue(retIDs.findIfIDnumberPresent("2152683378"))

    def test_successful_ID_rejection(self):
	    self.assertFalse(retIDs.findIfIDnumberPresent("2153443218")) #Ben's ID is not in the database

   # def test_audio_recorded(self):
	#    os.system("arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav")
	 #   self.assertTrue(os.path.exists("test.wav"))
    
    def test_image_capture(self):
	    camera=picamera.PiCamera()
	    camera.capture("test.jpg")
	    self.assertTrue(os.path.exists("test.jpg"))

   # def test_text_IP(self):
    #    self.assertTrue(textIP.textIPtoRahat("test string"))
    
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

 
if __name__ == '__main__':
    unittest.main()
