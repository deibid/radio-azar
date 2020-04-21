from gpiozero import PWMLED
from time import sleep
import threading


class DisplayController:

    KILL_THREAD = False
    thread = None

    DISPLAY_CONFIGURATIONS = [
        # [0, 0, 0, 0, 0],  # 0
        [1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 0, 0],  # 2
        [1, 1, 1, 0, 0],  # 3
        [1, 1, 1, 1, 0],  # 4
        [1, 1, 1, 1, 1]]  # 5

    BRIGHTNESS = 0.35

    def __init__(self):
        self.leds = [PWMLED(23), PWMLED(24), PWMLED(25), PWMLED(8), PWMLED(7)]
        self.recording_led = PWMLED(1)
        self.num_messages = 0

    def display_message_counter(self, num_messages):

        self.num_messages = num_messages
        if num_messages == 0:
            self.turn_off()
            return

        # rollover after 5 back to 1
        num_messages = (num_messages % 5) - 1
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
            self.turn_off()
            self.recording_led.pulse(fade_in_time=1, fade_out_time=1)
        else:
            self.recording_led.off()

    def increase_display_count(self):
        self.display_message_counter(self.num_messages+1)

    def decrease_display_count(self):
        self.display_message_counter(self.num_messages-1)

    def turn_off(self, fade_out=False):
        for l in self.leds:
            l.off()

    def display_loading(self, _sleep=.15, _in=.3, _out=.95):

        self.turn_off()
        for l in self.leds:
            l.pulse(fade_in_time=_in, fade_out_time=_out)
            sleep(_sleep)

    def stop_loading(self):

        self.turn_off()
