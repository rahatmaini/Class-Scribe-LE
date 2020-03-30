import json

def transcribe():
    with open ('test.json') as f:
        data = json.load(f)

    transcription=""
    
    for item in data['results']:
        transcription+=item['alternatives'][0]['transcript']
    #data=data['results'][0]['alternatives'][0]['transcript']
    return str(transcription)
    
