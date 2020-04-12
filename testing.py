from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-file.json'


def sample_recognize():

    client = speech_v1p1beta1.SpeechClient()

    #gsutil cp test.wav gs://classscribe


    storage_uri = 'gs://classscribe/test.wav'


    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
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

sample_recognize()