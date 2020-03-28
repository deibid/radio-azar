import subprocess
import os
import signal

class DRecorder:

  record_command = 'arecord -D hw:1,0  -f cd test.wav -c 1'

  def __init__(self):
    self.filename = 'voice.wav'
    pass

  def create_file_name(self):
    pass
    # self.filename = 'voice.wav'

  def prepare_file(self):
    self.create_file_name()
    self.record_command = 'arecord -D hw:1,0  -f cd '+ self.filename +' -c 1'

  def start_recording(self):
    print('start recording')
    self.prepare_file()

    # Fancy stuff to make subprocess terminable
    self.sp = subprocess.Popen(self.record_command, stdout=subprocess.PIPE, 
                          shell=True, preexec_fn=os.setsid) 


  def stop_recording(self):
    print('stop recording')
    os.killpg(os.getpgid(self.sp.pid), signal.SIGTERM)

  def play_recording(self):
    subprocess.Popen("aplay "+"fb-"+self.filename, shell=True)
    print('finished playing')

    
    


