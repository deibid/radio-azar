from gpiozero import PWMLED


class DisplayController:

  DISPLAY_CONFIGURATIONS = [
    [0,0,0,0,0], #0
    [1,0,0,0,0], #1
    [1,1,0,0,0], #2
    [1,1,1,0,0], #3
    [1,1,1,1,0], #4
    [1,1,1,1,1], #5
    [0,1,1,1,1], #6
    [0,0,1,1,1], #7
    [0,0,0,1,1], #8
    [0,0,0,0,1]] #9
  
  BRIGHTNESS = 0.35

  def __init__(self):
    self.leds = [PWMLED(23), PWMLED(24), PWMLED(25), PWMLED(8), PWMLED(7)]
    self.recording_led = PWMLED(1)
    self.num_messages = 0


  def display_message_counter(self,num_messages):
    
    self.num_messages = num_messages
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
      self.recording_led.pulse(fade_in_time = 1.2, fade_out_time = 1.5)
    else: 
      self.recording_led.off()


  def decrease_display_count(self):
    self.display_message_counter(self.num_messages-1)


    







  
