import pendulum
import datetime
from my_modules.DateUtils import DateUtils

class StorageUtils:

  # date_utils = DateUtils()

  def __init__(self):
    pass


  @staticmethod
  def generate_filename_for_local_recording(date,uuid):

    now = date.to_iso8601_string()
    valid_date_string = now.replace(":","-")
    valid_date_string = valid_date_string.replace(".","-")
    
    return uuid+"-"+valid_date_string+".wav"

  @staticmethod
  def get_path_for_local_system_recording():
    return "audio/my_recordings/"

  @staticmethod
  def generate_filename_for_local_storage_download(msg):

    date_string = msg.val()['time']
    valid_date_string = date_string.replace(":","-")
    valid_date_string = valid_date_string.replace(".","-")
    uuid = msg.val()['sender']

    # filename = uuid + "-"+dt+".wav"
    local_system_filename = "audio/others_recordings/"+ uuid + "-"+valid_date_string+".wav"
    # local_system_filename = uuid + "-"+valid_date_string+".wav"
    return local_system_filename
    

  @staticmethod
  def generate_filename_for_cloud_storage(timestamp, sender):

    date_string = timestamp
    valid_date_string = date_string.replace(":","-")
    valid_date_string = valid_date_string.replace(".","-")
    uuid = sender

    # filename = uuid + "-"+dt+".wav"
    cloud_system_filename = "audio/"+ uuid + "/"+uuid+"-"+valid_date_string+".wav"
    return cloud_system_filename





    



