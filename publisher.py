import pika
import json

# 파이썬에서 스프링으로
class Publisher:
    def __init__(self):
        self.__url = 'localhost' #'130.162.128.153'
        self.__port = 5672
        self.__vhost = '/'
        self.__cred = pika.PlainCredentials('admin', 'admin')
        self.__queue = 'response_q'
        return

    def main(self, message):
        response_message = {"movieRankList" : [message]}
        conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
        chan = conn.channel()
        chan.basic_publish(
            exchange='response_e',
            routing_key='ottRank',
            body=json.dumps(response_message)
        )
        conn.close()
        return

publisher = Publisher()