from google.cloud import vision
import io
import os

listOfWords=[]
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-file.json'

def detect_document():
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open("notesA1.jpg", 'rb') as image_file:
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


                    #for symbol in word.symbols:
                        #print('\tSymbol: {} (confidence: {})'.format(
                         #   symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


detect_document()
print (listOfWords)