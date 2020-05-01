import time
import subprocess


class AudioFile:
    def __init__(self, filename):
        self.filename = filename
        self.played = False

    def print(self):
        print('Filename-> ')
        print(self.filename)


class AudioPlayer:

    audio_files_to_play = None

    def __init__(self, display_controller):
        self.audio_files_to_play = []
        self.display_controller = display_controller

    def add_file(self, file):
        self.audio_files_to_play.append(file)

    def play_files(self):
        print('playing files')

        for f in self.audio_files_to_play:

            print('playing')
            # play and wait until finished before the next one
            self.display_controller.display_message_playing()
            subprocess.Popen("aplay "+f.filename, shell=True).wait()
            f.is_played = True
            self.display_controller.decrease_display_count()

            print('finished... playing next')

        self.audio_files_to_play = []

    def len(self):
        print('this many messages to play in audio player')
        print(len(self.audio_files_to_play))
        return len(self.audio_files_to_play)
