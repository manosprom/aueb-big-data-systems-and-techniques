from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
import json

access_token = "2612837631-AgcrWoBeA4QopCGWJROf62P6Nzo5dk2LaU5FUqM"
access_token_secret =  "vs5HkeoX5v6m1ujZYxlka2WTia21EgLlom3HWAM8rtvo2"
consumer_key =  "aAofHmy8se1EaWDLOAJ7JVA3h"
consumer_secret =  "o2CC5TGvIRWn2sLytmGpdIQvZkTYWPakkvDrZ8iAnI0jpIZrjS"

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("offers", data.encode('utf-8'))
        print ("=====================================================================================")
        parsed = json.loads(data)
        print(parsed['created_at'], "-", parsed['text'])
        print ("=====================================================================================")
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=[
    'shop shoes',
    'shopping shoes',
    'shopping offers shoes',
    'offers shoes',
    'sell shoes',
    'shoes offer',
    'shoes gift'
])