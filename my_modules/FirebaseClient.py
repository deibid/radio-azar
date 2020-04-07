import pyrebase
import datetime, time
from my_modules.DateUtils import DateUtils
import pendulum
# storage.child("audio/audio").put("rec-3.mp3")

class FirebaseClient:

    date_utils = DateUtils()
    
    firebase_config = {
       "apiKey": "",
        "authDomain": "",
        "databaseURL": "https://radio-test-1-dae0f.firebaseio.com/",
        "storageBucket": "radio-test-1-dae0f.appspot.com"
    }

    def __init__(self, drecorder, uuid):    
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.cloud_storage = self.firebase.storage()
        self.db = self.firebase.database()
        self.drecorder = drecorder
        self.uuid = uuid

    def write_database_with_file(self,url):
        
        print('attempting to write db')
        print('----------------------')

        ref = self.db.child("messages/")
        key = ref.generate_key()

        timestamp = pendulum.now().to_iso8601_string()


        data = {
            "playback-time":"tonight",
            "sender":self.uuid,
            "time": timestamp,
            "audioUrl":url
        }


        print(data)

        ref.push(data)

        print('db write succesfull')
        print('----------------------')



    def get_data_for_relevant_recordings(self):

        this_weeks_messages = []

        all_messages = self.db.child("messages").get()
        db_date = None

        low_range = self.date_utils.get_low_range_for_week()
        high_range  = self.date_utils.get_high_range_for_week()

        for message in all_messages.each():
                        
            # print(message.val()['playback-time'])
            # print(message.val()['time'])

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
        

        # query the database
        # filter entries to only leave the ones for this week
            # lograr aritmetica basica con fehcas
            # crear limites de la fecha

            # filtrar que todo este dentro de estos limites

        # objtener lista de urls
        # bajar los archivos correspondientes

        



        
        


    
    
    def download_file(self,filename):
        print('downloading file from Firebase')
        self.cloud_storage.child("audio/"+filename).download("fb-"+filename)
    
    def upload_file(self,filename):
        self.cloud_storage.child(self.drecorder.firebase_filename).put(self.drecorder.local_system_filename)
        fileUrl = self.cloud_storage.child(self.drecorder.firebase_filename).get_url("")
        self.write_database_with_file(fileUrl)
        print('file uploaded to ze cloud!')

    