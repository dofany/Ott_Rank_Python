import json
import pika
import sys
import subprocess

# 스프링에서 파이선으로
class Consumer:
    def __init__(self):
        self.__url = 'localhost' # '130.162.128.153'
        self.__port = 5672
        self.__vhost = '/'
        self.__cred = pika.PlainCredentials('admin', 'admin')
        self.__queue = 'request_q'
        return

    def on_message(self, channel, method_frame, header_frame, body):
        try:
            process = subprocess.Popen(['python3', 'allWebCrawling.py', body])
            process.communicate()  # 프로세스 실행이 완료될 때까지 대기하고 출력을 읽어옴
        except Exception as e:
            print('Exception occurred while processing message:', e)
            # 예외 처리를 원하는 방식으로 진행
            # 예를 들어, 예외가 발생하면 다음 메시지 처리로 넘어가거나, 프로세스 종료 등을 할 수 있습니다.
        finally:
            sys.exit()

    def main(self):
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
            chan = conn.channel()
            chan.basic_consume(
                queue=self.__queue,
                on_message_callback=self.on_message,
                auto_ack=True
            )
            chan.start_consuming()
        except Exception as e:
            print('Exception occurred during consuming:', e)
        return


consumer = Consumer()
consumer.main()