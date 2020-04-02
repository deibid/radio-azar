import pyrebase
import datetime
# storage.child("audio/audio").put("rec-3.mp3")

class FirebaseClient:
    
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
        timestamp = str(datetime.datetime.now())
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



    
    def download_file(self,filename):
        print('downloading file from Firebase')
        self.cloud_storage.child("audio/"+filename).download("fb-"+filename)
    
    def upload_file(self,filename):
        self.cloud_storage.child(self.drecorder.firebase_filename).put(self.drecorder.local_system_filename)
        fileUrl = self.cloud_storage.child(self.drecorder.firebase_filename).get_url("")
        self.write_database_with_file(fileUrl)
        print('file uploaded to ze cloud!')

    