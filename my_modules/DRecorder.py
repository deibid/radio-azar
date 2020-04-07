import subprocess
import os
import signal
import datetime, time, pendulum
from my_modules.StorageUtils import StorageUtils


class DRecorder:

  storage_utils = StorageUtils()
  record_command = 'arecord -D hw:1,0  -f cd test.wav -c 1'

  def __init__(self, uuid):
    self.uuid = uuid

  def create_file_name(self):
  
    
    self.date = pendulum.now()
    self.filename = self.storage_utils.generate_filename_for_local_recording(self.date, self.uuid)
    self.local_system_filename = self.storage_utils.get_path_for_local_system_recording()+self.filename
    self.firebase_filename = "audio/"+self.uuid+"/"+self.filename


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


  def get_timestamp(self):
    return self.date.to_iso8601_string()

    
    


