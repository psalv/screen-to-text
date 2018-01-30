import io
import os
import time

import pyscreenshot as ImageGrab
# from PIL import Image     # testing

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/paulsalvatore57/PycharmProjects/breakq/breakq-ab2f4dbb2437.json"


def take_screenshots():
    if __name__ == '__main__':

        # grab fullscreen
        img = ImageGrab.grab()
        # img = Image.open("tests/test1.png")     # testing

        # Crop the question
        question = img.crop((15, 170, 400, 520))

        # Save a file with just the question
        question.save("live.bmp")


def detect_text_uri():
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), 'live.bmp')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


run = raw_input("Start? > ")
start_time = time.time()

take_screenshots()
detect_text_uri()

print("Runtime:" + str(time.time() - start_time))
