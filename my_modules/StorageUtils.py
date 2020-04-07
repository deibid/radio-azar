import pendulum
import datetime
from my_modules.DateUtils import DateUtils

class StorageUtils:

  date_utils = DateUtils()

  def __init__(self):
    pass
  
  @staticmethod
  def generate_filename_for_local_storage_download(msg):

    date_string = msg.val()['time']
    valid_date_string = date_string.replace(":","-")
    valid_date_string = valid_date_string.replace(".","-")
    uuid = msg.val()['sender']

    # filename = uuid + "-"+dt+".wav"
    local_system_filename = "audio/others_recordings/"+ uuid + "-"+valid_date_string+".wav"
    
    print("file will output to:\n\n")
    print(local_system_filename)




