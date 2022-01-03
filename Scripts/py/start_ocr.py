from google.oauth2 import service_account
from google.cloud import vision
from pygame.locals import * 
from subprocess import call
from gpiozero import Button
import sys
from signal import pause
import pygame.camera
#from textblob import TextBlob
import subprocess
import random
import numpy as np
import pyttsx3
from gtts import gTTS
import argparse
import time
import cv2
"""import playsound"""
import io
import os
from textblob import TextBlob
from googletrans import Translator
#from translate import Translator
from langdetect import detect


def gtts_speak(text):
    
    #var = detect(text)
    #print(var)
    #text = text.replace("- ", "")
    #text = text.replace("-  ", "")
    #blob = TextBlob(text)
    #print(blob)
    
    #translator= Translator(to_lang="Bulgarian")
    #translation = translator.translate(text)
    #print(translation)
    
    if text != "":
        #tts = gTTS(text, lang=var)
        #print(detect(text))
        #language = detect(text)
        #tts = gTTS(text, lang=language)
        #tts.save('page.mp3')
        #os.system('mpg321 page.mp3 &')
        
        engine = pyttsx3.init()
        
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 110)
        
        engine.say(text)
        engine.runAndWait()

    else:
        errorMessages = ["ocr_error_1.mp3",
                         "ocr_error_2.mp3",
                         "ocr_error_3.mp3"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        os.system('mpg321 ' + '/home/pi/error_messages/' + chosen_message + ' &')


def call_google_api_ocr():
    imageUrl = "/home/pi/Desktop/output-1.jpg"
    client = "/home/pi/client_id.json"
        
    # Connecting to the Google Vision API
    credentials = service_account.Credentials.from_service_account_file(
    filename = client,
    scopes = ["https://www.googleapis.com/auth/cloud-platform"])

    client = vision.ImageAnnotatorClient(credentials=credentials)

    #image = take_picture()
    with io.open(imageUrl, "rb") as f:
        byteImage = f.read()

    # Sending Image as ByteImage to the API
    print("Making request to Google Vision API OCR...")
    image = vision.Image(content=byteImage)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on errors, check:\n"
            "https://cloud.google.com/apis/design/errors".format(
            response.error.message))


    # Load returned text
    image = cv2.imread(imageUrl)
    final = image.copy()

    for text in response.text_annotations[1::]:

        ocr = text.description

        with open('/home/pi/result.txt', 'a', encoding='utf-8') as f:
            f.write(ocr + " ")

        startX = text.bounding_poly.vertices[0].x
        startY = text.bounding_poly.vertices[0].y
        endX = text.bounding_poly.vertices[1].x
        endY = text.bounding_poly.vertices[2].y
        rect = (startX, startY, endX, endY)

    lines = []
    with open('/home/pi/result.txt', 'r', encoding='utf-8') as f:
        lines = f.read()

    print(lines)

    gtts_speak(lines)
    #speak(lines)

    with open('/home/pi/result.txt', 'w', encoding='utf-8') as f:
            f.write("")

    # Show final image
    #output = image.copy()
    #output = draw_ocr_results(output, ocr, rect)
    #final = draw_ocr_results(final, ocr, rect)

    #cv2.imshow("Output", output)
    #cv2.waitKey(0)

    #cv2.imshow("Final Output", final)
    #cv2.waitKey(0)

    print("OCR Finished Executing!")
    
    
if __name__ == '__main__':
    call_google_api_ocr()
    sys.exit()