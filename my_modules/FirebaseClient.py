import pyrebase
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
        self.drecorder = drecorder
        self.uuid = uuid

    
    def download_file(self,filename):
        print('downloading file from Firebase')
        self.cloud_storage.child("audio/"+filename).download("fb-"+filename)
    
    def upload_file(self,filename):


        self.cloud_storage.child(self.drecorder.firebase_filename).put(self.drecorder.local_system_filename)
        print('file uploaded to ze cloud!')

    