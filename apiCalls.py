import requests
import datetime
import json
base_url = 'http://128.143.67.97:44104/'



def uploadAudio(file, author, class_name, length, timestamp):
	url = base_url + "api/audioupload/"
	audio = open(file, 'rb')
	files = {
		"file": audio
	}
	data = {
		"remark": str(datetime.datetime.now())[0:15],
		"class_name": class_name,
		"length": length,
		"timestamp": timestamp
	}
	res = requests.request('POST', url, data=data, files=files)
	print (res.text)
	return res.json()['key']

#uploadAudio("test.wav", "123", "uh", "5", str(datetime.datetime.now()))

def createImage(filename, email, class_name, page_num, timestamp):
    url = base_url + 'upload/'
    img = open(filename, 'rb')
    files = {
		"file": img
	}
    data = {
		"remark": email,
		"class_name": class_name,
		"page_num": page_num,
		"timestamp": timestamp,
        "lampSN": 1
	}
    res = requests.request('POST', url, data=data, files=files)
    print (res.text)
    return res.json()['pk']

#createImage("1.jpg","rm4mp@virginia.edu","uh","1", datetime.datetime.now())

def createNotebook(private, class_name, notebookname, user_pk):
    url = base_url + 'notebooks/create/'
    data = {
		"Private": private,
		"class_name": class_name,
		"name": notebookname,
		"pk": user_pk
	}
    res = requests.request('POST', url, data=data)
    return res.json()['key']

def createPage(time, name, notebook_pk):
	url = base_url + 'notebooks/create/page/'
	data ={
		'time': time,
		'name': name,
		'pk': notebook_pk
	}
	res = requests.request('POST', url, data=data)
	#print(res.text)
	return res.json()['key']

def addImagestoPage(page_pk, image_pks, image_author, class_name):
    url = base_url + 'notebooks/add/'
    data ={
		'pk': page_pk,
		'image_pks': image_pks,
		'remark': image_author,
		'class_name': class_name
	}
    print ("IMAGE PKs passed in: ", image_pks)
    res=requests.request('POST', url, data=data)
    print (res.json())
    
def addAudioAndTranscription(pk_audio, pk_page, transcript):
	url = base_url + 'notebooks/add/audio/'
	data = {
		"pk_audio": pk_audio,
		"pk_page": pk_page,
		"transcript": transcript
	}
	print(requests.request('POST', url, data=data).text)

#for i in range(4):
#	print(createImage(str(i+1)+'.jpg', "jw2vp@virginia.edu", 'CS 1110', i, datetime.datetime.now())['pk'])

# user = requests.request('GET', base_url + 'api/user/').json()
# print(user)


# getting user pk
#card_id = 123456
#res = requests.request('GET', base_url + 'api/getUserEmailAndPKByID/' + str(card_id)).json()
#user_pk = res['pk']
#user_email = res['email']
#class_name = 'CS 1110'
#notebook_name = datetime.datetime.now()
#creating notebook

#nb_pk = createNotebook(False, class_name, notebook_name, user_pk)

#for each image, we should have the pk in a list of lists that mirrors the list of lists with names of the files
#so like [[1,2,3],[4,5,6],[7,8,9]] is the list of pks and list of image names [['duckbutter.jpg', 'ibrahim.jpg', 'eddy.jpg'],..
# and the pk that equals 1 is the primary key on the server for the image created for duckbutter.jpg


#images = [[]] #list of list with names of all images (or "image" objects that have time taken as well as name)
#image_pks = [[]] # createImage('blahblah')['pk'], this will get you the pk for a create image so you have it for later

#have to add audio and transcript to first page
#date = str(datetime.datetime.now()).split()[0]
#first_page_pk = createPage(date, str(datetime.datetime.now()), nb_pk)

#upload audio
#lengthOfAudio = '4500' #don't know if we need this, number of seconds in 1 hour and 15 mins
#audio_name = 'audio.wav'
#audio_pk = uploadAudio(audio_name, user_email, class_name, lengthOfAudio)

#transcript = 'something'

#addAudioAndTranscription(audio_pk, first_page_pk, transcript)

#for i in range(len(images)):
#	page_pk = createPage(date, str(datetime.datetime.now()), nb_pk)
#	addImagestoPage(page_pk, image_pks[i], user_email, class_name)





