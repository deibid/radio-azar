from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint


EVENT_UPLOADED_MESSAGE = "message_uploaded"
UUID = "david"

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-5640dcb4-620c-11ea-9a99-f2f107c29c38"
pnconfig.publish_key = "pub-c-3c259a14-9e90-49f0-bf85-03615209e485"
pnconfig.uuid = UUID

class PubNubClient:

    # PubNub configurations
    class NewMessageSubscribeCallback(SubscribeCallback):

        def __init__(self,firebase_client,drecorder):
            self._firebase_client = firebase_client
            self._drecorder = drecorder

        def status(self, pubnub, status):
            pass

        def presence(self, pubnub, presence):
            pprint(presence.__dict__)

        def message(self, pubnub, message):
            print('message!!!!!!!!!!!!!')
        
            if message.__dict__["message"]["content"] == "message_uploaded":
                print('alguien publicó un nuevo archivo')
                if message.__dict__["message"]["sender"] == pnconfig.uuid:
                    print("alguien que no eres tu mandó un mensaje")
                    self._firebase_client.download_file('voice.wav')
                    self._drecorder.play_recording()
                    
            pprint(message.__dict__)

    def __init__(self,firebase_client, drecorder):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.add_listener(self.NewMessageSubscribeCallback(firebase_client,drecorder))
        self.pubnub.subscribe()\
            .channels("pubnub_onboarding_channel")\
            .with_presence()\
            .execute()

        # self.firebase_client = firebase_client  
        # self.drecorder = drecorder

    def publish_callback(self,envelope, status):
        print('full circle')
        print(envelope, status)

    def broadcastUploadedMessage(self):
        self.pubnub.publish()\
            .channel("pubnub_onboarding_channel")\
            .message({"sender": pnconfig.uuid, "content": EVENT_UPLOADED_MESSAGE})\
            .pn_async(self.publish_callback)


    

    
