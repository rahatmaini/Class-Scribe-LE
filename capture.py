import subprocess
import time
import threading
import requests
import datetime
import transcribe
import apiCalls
import os
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-file.json'

snapshots = [] #list of dictionaries
pages = []


def audioRecord(filename):
	test2 = subprocess.Popen(["arecord", "--device=hw:1,0", "--format", "S16_LE", "--rate", "44100", "-c", "2", "--duration=30", filename], stdout=subprocess.PIPE) # DURATION!!
	output2 = test2.communicate()[0]


def takePhotos():
	t0 = time.time()
	flag = 1
 
	while (time.time() - t0 >= 30):
		snapDict = {}
		picFilename = str(time.time())+".jpg"
		test = subprocess.Popen(["raspistill","-o",picFilename],stdout=subprocess.PIPE)
		snapDict["timestamp"]=(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
		output = test.communicate()[0]
		snapDict["filename"]=picFilename
		snapDict["isThisFinalSnapshot"]=False #set true if Arduino microphone catches page flip
		
		snapshots.append(snapDict)


def capture(className, email, pk):
	timeStampedFileName=str(time.time()).replace(".","")+".wav" #for audio

	t1 = threading.Thread(target=audioRecord, args=(timeStampedFileName,))
	t2 = threading.Thread(target=takePhotos, args=())

	t1.start()
	t2.start()
	t1.join()
	t2.join()

	uploadFiles(timeStampedFileName, className, email, pk)
	

def transcribeAudio(filename):
	client = speech_v1p1beta1.SpeechClient()

	if os.system("gsutil cp "+ filename + " gs://classscribe") == 0:
		pass
	else:
		print ("Could not upload file to Google Cloud")
		return ("Resource Overflow")

	storage_uri = 'gs://classscribe/'+filename


	encoding = enums.RecognitionConfig.AudioEncoding.MP3
	config = {
		"language_code": "en-US",
		"sample_rate_hertz": 44100,
		"encoding": encoding,
	}
	audio = {"uri": storage_uri}

	#response = client.recognize(config, audio)

	operation = client.long_running_recognize(config, audio)
	print(u"Waiting for operation to complete...")
	response = operation.result()


	for result in response.results:
		alternative = result.alternatives[0]
		return (alternative.transcript) 

def extractHandwriting(filename):
	client = vision.ImageAnnotatorClient()
	listOfWords = []
	
	with io.open(filename, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.document_text_detection(image=image)

	for page in response.full_text_annotation.pages:
		for block in page.blocks:
			print('\nBlock confidence: {}\n'.format(block.confidence))

			for paragraph in block.paragraphs:
				print('Paragraph confidence: {}'.format(
					paragraph.confidence))

				for word in paragraph.words:
					word_text = ''.join([
						symbol.text for symbol in word.symbols
					])
					#print('Word text: {} (confidence: {})'.format(word_text, word.confidence))
					listOfWords.append(word_text)

	if response.error.message:
		raise Exception(
			'{}\nFor more info on error messages, check: '
			'https://cloud.google.com/apis/design/errors'.format(
				response.error.message))

	return listOfWords
	
	
def uploadFiles(filename, className, email, pk):

	audioPK=apiCalls.uploadAudio(filename, email, className, "5", str(datetime.datetime.now())) #file, author, class_name, length, timestamp
	notebookPK = apiCalls.createNotebook(False, className, className, pk) #private, class_name, notebookname, user_pk
	transcript = str(transcribeAudio(filename)) #transcript is the same over entire session

	#
	#
	# for loop here to read from Arduino and set finalSnapshot boolean and then doc scan
	#
	#
	
	indexOfFirstSnap=0 #watch out for index out of bounds errors that might happen here
	for pic in snapshots: 

		pic["pk"] = int(apiCalls.createImage(pic["filename"], email, className, "1", pic["timestamp"]))

		if (pic["isThisFinalSnapshot"]):
			pageDict={}
			pageDict["snapshots"] = snapshots[indexOfFirstSnap:snapshots.index(pic)+1] #from first snap to the last in page
			indexOfFirstSnap = snapshots.index(pic)
			
			pageDict["handwriting"] = str(extractHandwriting(pic["filename"]))
			pageDict["name"] = pic["filename"]
			
			pages.append(pageDict)
	

	for page in pages:
		page["pk"] = apiCalls.createPage(str(datetime.datetime.now()).split()[0],str(datetime.datetime.now()),notebookPK) 

		for image in page["snapshots"]:
			apiCalls.addImagestoPage(int(page["pk"]), image["pk"], email, className)
		

		apiCalls.addAudioAndTranscription(audioPK,int(page["pk"]), transcript)

	

	 
	


