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

    display_controller = None

    # PubNub configurations
    class NewMessageSubscribeCallback(SubscribeCallback):

        def __init__(self, firebase_client, drecorder, display_controller):
            self.firebase_client = firebase_client
            # self._drecorder = drecorder
            self.display_controller = display_controller

        def status(self, pubnub, status):
            pass

        def presence(self, pubnub, presence):
            pprint(presence.__dict__)

        def message(self, pubnub, message):

            print('\n')
            print('message from pubnub received')
            print('\n')

            if message.__dict__["message"]["content"] == "message_uploaded":
                # self.display_controller.stop_loading()
                num_messages = self.firebase_client.num_relevant_recordings()
                self.display_controller.display_message_counter(num_messages)
                # if message.__dict__["message"]["sender"] == pnconfig.uuid:
                # pass
                # self._firebase_client.fetch_relevant_recordings()

    def __init__(self, firebase_client, drecorder, display_controller):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.add_listener(
            self.NewMessageSubscribeCallback(firebase_client, drecorder, display_controller))
        self.pubnub.subscribe()\
            .channels("pubnub_onboarding_channel")\
            .with_presence()\
            .execute()

        # self.firebase_client = firebase_client
        self.drecorder = drecorder
        self.display_controller = display_controller

    def publish_callback(self, envelope, status):
        # print('full circle')
        print('\n')
        print('pubnub message published')
        print('\n')
        # print(envelope, status)

    def broadcastUploadedMessage(self):
        self.pubnub.publish()\
            .channel("pubnub_onboarding_channel")\
            .message({"sender": pnconfig.uuid, "content": EVENT_UPLOADED_MESSAGE, "url": self.drecorder.firebase_filename})\
            .pn_async(self.publish_callback)
