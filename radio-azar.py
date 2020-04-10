# from recorder import Recorder
from gpiozero import Button
from signal import pause
from time import sleep
from datetime import datetime
import os
import pygame
import pyrebase
from enum import Enum

from my_modules.FirebaseClient import FirebaseClient
from my_modules.PubNubClient import PubNubClient
from my_modules.DRecorder import DRecorder
from my_modules.DisplayController import DisplayController

# Owner of this device.
from my_modules.PubNubClient import UUID


record_button = Button(2, hold_time = 1.5)
# play_button = Button(3)


display_controller = DisplayController()
drecorder = DRecorder(UUID,display_controller)
firebase_client = FirebaseClient(drecorder,UUID,display_controller)
pubnub_client = PubNubClient(firebase_client,drecorder)


class States(Enum):
    stand_by = 0
    recording = 1
    playing = 2

state = States.stand_by

# is_recording = False


def main():
    print("app is ready")
    
def start_recording():
    drecorder.start_recording()

def finish_recording():

    drecorder.stop_recording()
    firebase_client.upload_file(drecorder.filename)
    pubnub_client.broadcastUploadedMessage()

def download_file():
    print("play pressed")
    firebase_client.download_file('voice.wav','voice.wav')


def play_files():
    global state
    state = States.playing
    print("started playing with held")

    # pygame.mixer.music.load(drecorder.filename)
    # pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy():
    #     sleep(1)
    # print("finished playing")

# Audio setup. possibly might go away
pygame.mixer.init()

if __name__ == "__main__":
    main()


def get_entries():
    print('get entries')
    firebase_client.fetch_relevant_recordings()

def handle_button_release():
    
    global state

    if state == States.playing:
        print('estas playing, no hagas nada')
        return

    elif state == States.stand_by:
        print('recording is going to start')
        state = States.recording
        # start_recording()
    elif state == States.recording:
        print('recording is going to finish')
        # finish_recording()
        state = States.stand_by
        

    # is_recording = not is_recording


# GPIO Events
# record_button.when_pressed = get_entries
# record_button.when_pressed = start_recording
# record_button.when_released = finish_recording

record_button.when_released = handle_button_release
record_button.when_held = play_files

# play_button.when_pressed = playFiles
# play_button.when_pressed = download_file
# play_button.when_pressed = get_entries
# Listen for events
pause()


