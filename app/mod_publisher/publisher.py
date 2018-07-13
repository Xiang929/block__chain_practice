import zmq
import asyncio
import zmq.asyncio
from zmq.error import ZMQError
from config import *


class Publisher(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('tcp://{0}:{1}'.format(host, port))

    def publiser_rep(self):
        context = zmq.Context.instance()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://{0}:{1}'.format(SERVER, WRITE_PORT))

        while True:
            [topic, body] = socket.recv_multipart()
            socket.send(b'recived')
            if topic == b'new block':
                self.publiser_publish(topic, body)
            elif topic == b'new block finished':
                self.publiser_publish(topic, body)
            elif topic == b'modify block':
                self.publiser_publish(topic, body)
            elif topic == b'modify block finished':
                self.publiser_publish(topic, body)
            else:
                pass

    def publiser_publish(self, topic, body):
        print(topic, body)
        if topic == b'new block':
            self.socket.send_multipart([topic, body])
            print('send')
        elif topic == b'new block finished':
            self.socket.send_multipart([b'creat block', body])
        elif topic == b'modify block':
            self.socket.send_multipart([topic, body])
        elif topic == b'modify block finished':
            self.socket.send_multipart([b'replace blockchain', body])
        else:
            pass


if __name__ == '__main__':
    publisher = Publisher(SERVER, PORT)
    publisher.publiser_rep()
