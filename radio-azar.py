# from recorder import Recorder
from gpiozero import Button
from signal import pause
from time import sleep
from datetime import datetime
import os
import pygame
import pyrebase

from my_modules.FirebaseClient import FirebaseClient
from my_modules.PubNubClient import PubNubClient
from my_modules.DRecorder import DRecorder

# Owner of this device.
from my_modules.PubNubClient import UUID


record_button = Button(2)
play_button = Button(3)


drecorder = DRecorder(UUID)
firebase_client = FirebaseClient(drecorder,UUID)
pubnub_client = PubNubClient(firebase_client,drecorder)



def main():
    print("app is readygit")
    
def start_recording():
    drecorder.start_recording()
    print('recording started...')


def finish_recording():

    drecorder.stop_recording()
    print('recording stopped...')
    firebase_client.upload_file(drecorder.filename)
    pubnub_client.broadcastUploadedMessage()

def download_file():
    print("play pressed")
    firebase_client.download_file('voice.wav','voice.wav')


def playFiles():
    print("started playing")
    pygame.mixer.music.load(drecorder.filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)
    print("finished playing")

# Audio setup. possibly might go away
pygame.mixer.init()

if __name__ == "__main__":
    main()


def get_entries():
    print('get entries')
    firebase_client.fetch_relevant_recordings()


# GPIO Events
# record_button.when_pressed = get_entries
record_button.when_pressed = start_recording
record_button.when_released = finish_recording

# play_button.when_pressed = playFiles
# play_button.when_pressed = download_file
play_button.when_pressed = get_entries
# Listen for events
pause()


