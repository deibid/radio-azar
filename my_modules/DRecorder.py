import subprocess
import os
import signal
import datetime, time


class DRecorder:

  record_command = 'arecord -D hw:1,0  -f cd test.wav -c 1'

  def __init__(self, uuid):
    self.uuid = uuid

  def create_file_name(self):

    dt = datetime.datetime.now()
    dt = dt.strftime("%c")
    dt = dt.replace(" ","-")
    dt = dt.replace(":","-")
    
    self.filename = self.uuid + "-"+dt+".wav"
    self.local_system_filename = "audio/my_recordings/"+self.uuid + "-"+dt+".wav"
    self.firebase_filename = "audio/"+self.uuid+"/"+self.filename
    self.timestamp = time.time()

    print("Filename->   "+self.filename)

  def prepare_file(self):
    self.create_file_name()
    self.record_command = 'arecord -D hw:1,0  -f cd '+ self.local_system_filename +' -c 1'

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

    
    


