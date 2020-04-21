# from recorder import Recorder
from gpiozero import Button
from signal import pause
from time import sleep
from datetime import datetime
import os
import pyrebase
from enum import Enum

from my_modules.FirebaseClient import FirebaseClient
from my_modules.PubNubClient import PubNubClient
from my_modules.DRecorder import DRecorder
from my_modules.DisplayController import DisplayController
from my_modules.AudioPlayer import AudioPlayer
# Owner of this device.
from my_modules.PubNubClient import UUID

display_controller = DisplayController()
audio_player = AudioPlayer(display_controller)
drecorder = DRecorder(UUID, display_controller)
firebase_client = FirebaseClient(drecorder, UUID, audio_player)
pubnub_client = PubNubClient(firebase_client, drecorder, display_controller)


record_button = Button(2, bounce_time=0.0018, hold_time=1.5)


class States(Enum):
    stand_by = 0
    recording = 1
    playing = 2


state = States.stand_by


def main():
    print("app is ready")
    initialize_display()


def start_recording():
    drecorder.start_recording()


def finish_recording():

    display_controller.display_loading()
    drecorder.stop_recording()
    print('before fc upload in main')
    sleep(1)

    firebase_client.upload_file(drecorder.filename)
    display_controller.stop_loading()
    pubnub_client.broadcastUploadedMessage()

    drecorder.clear_filenames()

    # num_messages = audio_player.len()
    # display_controller.display_message_counter(num_messages)


def download_file():
    print("play pressed")
    firebase_client.download_file('voice.wav', 'voice.wav')


def play_files():
    global state
    state = States.playing
    print("started playing with held")


def initialize_display():
    num_messages = firebase_client.num_relevant_recordings()
    display_controller.display_message_counter(num_messages)


if __name__ == "__main__":
    main()


def get_entries():

    global state

    if state != States.stand_by:
        print('was not in stand_by, will not play recordings')
        return

    print('get entries')
    state = States.playing
    # return

    display_controller.display_loading()
    firebase_client.fetch_relevant_recordings()

    num_messages = audio_player.len()
    display_controller.stop_loading()
    display_controller.display_message_counter(num_messages)

    # temporal, move to a play_file funciton
    audio_player.play_files()

    state = States.stand_by


def handle_button_release():

    global state

    if state == States.playing:
        print('estas playing, no hagas nada')
        return

    elif state == States.stand_by:
        print('recording is going to start')
        state = States.recording
        # sleep(0.02)
        start_recording()
    elif state == States.recording:
        print('recording is going to finish')
        # sleep(0.02)
        length = drecorder.get_recording_length()
        if length > 2:
            finish_recording()
            state = States.stand_by
        else:
            print('ignored press, recording too short')


# GPIO Events
record_button.when_released = handle_button_release
# record_button.when_held = play_files
record_button.when_held = get_entries
# Listen for events
pause()
