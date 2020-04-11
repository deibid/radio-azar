import pyrebase
import datetime, time
import pendulum

from my_modules.DateUtils import DateUtils
from my_modules.StorageUtils import StorageUtils
from my_modules.AudioPlayer import AudioFile, AudioPlayer


class FirebaseClient:

    date_utils = DateUtils()
    storage_utils = StorageUtils()
    
    firebase_config = {
       "apiKey": "",
        "authDomain": "",
        "databaseURL": "https://radio-test-1-dae0f.firebaseio.com/",
        "storageBucket": "radio-test-1-dae0f.appspot.com"
    }

    def __init__(self, drecorder, uuid, audio_player):    
        
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.cloud_storage = self.firebase.storage()
        self.db = self.firebase.database()
        self.drecorder = drecorder
        self.uuid = uuid
        self.audio_player = audio_player


    def write_database_with_file(self,url):
        
        ref = self.db.child("messages/")
        key = ref.generate_key()

        timestamp = self.drecorder.get_timestamp()
        cloud_path = self.storage_utils.generate_filename_for_cloud_storage(timestamp,self.uuid)


        data = {
            "playback-time":"tonight",
            "sender":self.uuid,
            "time": timestamp,
            "audioUrl":url,
            "cloud-path":cloud_path
        }


        print(data)

        ref.push(data)

        print('\n')
        print('----------------------')
        print('db write succesfull')
        print('----------------------')
        print('\n')



    def get_data_for_relevant_recordings(self):

        this_weeks_messages = []

        all_messages = self.db.child("messages").get()
        db_date = None

        low_range = self.date_utils.get_low_range_for_week()
        high_range  = self.date_utils.get_high_range_for_week()

        for message in all_messages.each():
            db_date = pendulum.parse(message.val()['time'])
        
            if db_date >= low_range and db_date < high_range:
                # turn on this line if you want to exclude your messages
                # if(message.val()["sender"] != self.uuid)
                this_weeks_messages.append(message)

        
        # sorts the messages based on time. First message sent is at the top and last at the bottom
        this_weeks_messages = sorted(this_weeks_messages, key=self.date_utils.sort_criteria)
        return this_weeks_messages



    def fetch_relevant_recordings(self):

        this_weeks_messages = self.get_data_for_relevant_recordings()


        for msg in this_weeks_messages:
            local_filename = self.storage_utils.generate_filename_for_local_storage_download(msg)
            remote_path = msg.val()['cloud-path']
            self.download_file(remote_path,local_filename)

            audio_file = AudioFile(local_filename)
            self.audio_player.add_file(audio_file)


        # num_msgs = len(this_weeks_messages)
        # self.display_controller.display_message_counter(num_msgs)        
    

    def download_file(self,remote_url, local_filename):
        
        self.cloud_storage.child(remote_url).download(local_filename)
        
        print('\n')
        print('file downloaded from Firebase')
        print(local_filename)
        print('\n')

    
    
    def upload_file(self,filename):

        self.cloud_storage.child(self.drecorder.firebase_filename).put(self.drecorder.local_system_filename)
        fileUrl = self.cloud_storage.child(self.drecorder.firebase_filename).get_url("")
        self.write_database_with_file(fileUrl)
        
        print('\n')
        print('file uploaded Firebase')
        print('\n')

    