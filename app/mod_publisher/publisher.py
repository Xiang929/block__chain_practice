import zmq
import zmq.asyncio
from config import *


class Publisher(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('tcp://{0}:{1}'.format(host, port))
        self.new_block_flag = False
        self.modify_block_flag = False

    def publisher_rep(self):
        context = zmq.Context.instance()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://{0}:{1}'.format(SERVER, WRITE_PORT))

        while True:
            [topic, body] = socket.recv_multipart()
            print(topic, body)
            socket.send(b'received')
            if topic == b'new block':
                self.new_block_flag = False
                self.publisher_publish(topic, body)
            elif topic == b'new block finished':
                self.new_block_flag = True
                self.publisher_publish(topic, body)
            elif topic == b'modify block':
                self.modify_block_flag = False
                self.publisher_publish(topic, body)
            elif topic == b'modify block finished':
                self.modify_block_flag = True
                self.publisher_publish(topic, body)
            else:
                pass

    def publisher_publish(self, topic, body):
        if topic == b'new block':
            self.socket.send_multipart([topic, body])
        elif topic == b'new block finished':
            self.socket.send_multipart([b'create block', body])
        elif topic == b'modify block':
            self.socket.send_multipart([topic, body])
        elif topic == b'modify block finished':
            self.socket.send_multipart([b'replace blockchain', body])
        else:
            pass


if __name__ == '__main__':
    publisher = Publisher(SERVER, PORT)
    publisher.publisher_rep()
