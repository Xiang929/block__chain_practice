import json

import zmq
import zmq.asyncio

from config import *


class Publisher(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUB)
        self.chain = []
        self.socket.bind('tcp://{0}:{1}'.format(host, port))
        self.index_list = []

    def publisher_rep(self):
        context = zmq.Context.instance()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://{0}:{1}'.format(SERVER, WRITE_PORT))

        while True:
            [topic, body] = socket.recv_multipart()
            print(topic, body)
            if topic == b'new block':
                self.publisher_publish(topic, body)
                socket.send(b'received')
            elif topic == b'new block finished':
                block_string = bytes.decode(body)
                block_obj = json.loads(block_string)
                if block_obj['index'] not in self.index_list:
                    self.index_list.append(block_obj['index'])
                    self.chain.append(block_obj)
                    self.publisher_publish(topic, body)
                socket.send(b'received')
            elif topic == b'modify block':
                self.publisher_publish(topic, body)
                socket.send(b'received')
            elif topic == b'modify block finished':
                self.publisher_publish(topic, body)
                socket.send(b'received')
            elif topic == b'synchronizing information':
                socket.send_pyobj(self.chain)
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
