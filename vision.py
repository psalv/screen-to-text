import io
import os
import webbrowser
import time
import sys

import pyscreenshot as ImageGrab
from PIL import Image                # testing

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/paulsalvatore57/PycharmProjects/breakq/breakq-ab2f4dbb2437.json"


def take_screenshots():
    if __name__ == '__main__':

        # grab fullscreen
        img = ImageGrab.grab()                     # Live
        # img = Image.open("tests/test7.png")        # Testing A
        # img = Image.open("tests_alt/test2.png")    # Testing B

        # Crop the question
        if len(sys.argv) > 1 and sys.argv[1] == 1:
            question = img.crop((15, 170, 400, 520))    # Question and answers
        else:
            question = img.crop((15, 390, 400, 750))    # Question and answers

        # Save a file with just the question
        question.save("live.bmp")


def build_google_search(query):
    search_url = "https://www.google.ca/search?q="
    for i in query.split():
        search_url += i + "+"
    return search_url


def detect_text_uri(openBrowser=False):
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

    lines = texts[0].description.split('\n')

    question = ""
    for i in range(len(lines) - 4):
        question += str(lines[i]) + " "

    answers = (str(lines[len(lines) - 4]), str(lines[len(lines) - 3]), str(lines[len(lines) - 2]))

    if openBrowser:
        webbrowser.open(build_google_search(question), new=0, autoraise=True)

    print question
    print answers

    # return question, answers


run = raw_input("Start? > ")

start_time = time.time()

take_screenshots()
detect_text_uri(True)

print("Runtime:" + str(time.time() - start_time))
