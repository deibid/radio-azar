from gpiozero import PWMLED
from time import sleep
import threading


class DisplayController:

    KILL_THREAD = False
    thread = None

    DISPLAY_CONFIGURATIONS = [
        [0, 0, 0, 0, 0],  # 0
        [1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 0, 0],  # 2
        [1, 1, 1, 0, 0],  # 3
        [1, 1, 1, 1, 0],  # 4
        [1, 1, 1, 1, 1],  # 5
        [0, 1, 1, 1, 1],  # 6
        [0, 0, 1, 1, 1],  # 7
        [0, 0, 0, 1, 1],  # 8
        [0, 0, 0, 0, 1]]  # 9

    BRIGHTNESS = 0.35

    def __init__(self):
        self.leds = [PWMLED(23), PWMLED(24), PWMLED(25), PWMLED(8), PWMLED(7)]
        self.recording_led = PWMLED(1)
        self.num_messages = 0

    def display_message_counter(self, num_messages):

        self.num_messages = num_messages
        # truncate the max led to 9
        if num_messages > 9:
            num_messages = 9

        config = self.DISPLAY_CONFIGURATIONS[num_messages]

        i = 0
        for c in config:
            print(c)
            if c:
                self.leds[i].value = self.BRIGHTNESS
            else:
                self.leds[i].off()
            i = i+1

    def display_recording(self, rec=False):

        if(rec):
            self.recording_led.pulse(fade_in_time=1, fade_out_time=1)
        else:
            self.recording_led.off()

    def increase_display_count(self):
        self.display_message_counter(self.num_messages+1)

    def decrease_display_count(self):
        self.display_message_counter(self.num_messages-1)

    def turn_off(self):
        for l in self.leds:
            l.off()

    def run_loading_sequence(self):

        i = 0
        mode = 'up'
        while self.KILL_THREAD != True:

            self.turn_off()
            self.leds[i].value = self.BRIGHTNESS

            if mode == 'up':
                i = i + 1
            elif mode == 'down':
                i = i - 1

            if i == 0:
                mode = "up"

            if i == 4:
                mode = 'down'

            sleep(.3)

    def display_loading(self):

        self.thread = threading.Thread(target=self.run_loading_sequence)
        self.thread.start()

    def stop_loading(self):
        self.KILL_THREAD = True
        self.thread.join()
        self.turn_off()
