import functools
import signal

import zmq
import zmq.asyncio
import json
import asyncio
from config import *

from app.mod_commodity.blockchain import Blockchain


class Subscriber(object):
    def __init__(self, host, port):
        self.loop = asyncio.get_event_loop()
        self.zmqContext = zmq.Context()
        self.blockchain = Blockchain()
        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.zmqSubSocket.connect("tcp://%s:%s" % (host, port))

    def handle(self):
        [topic, body] = self.zmqSubSocket.recv_multipart()
        print(topic, body)
        if topic == b'new block':
            transactions_string = bytes.decode(body)
            transactions = json.loads(transactions_string)
            new_block = self.blockchain.new_block(transactions)
            self.send_message('new block finished', new_block)
        elif topic == b'creat block':
            block_string = bytes.decode(body)
            block_obj = json.loads(block_string)
            self.blockchain.add_block(block_obj)
        elif topic == b'modify block':
            transactions_string = bytes.decode(body)
            transactions = json.loads(transactions_string)
            modify_dict = self.blockchain.modify_block(transactions)
            self.send_message('modify block finished', modify_dict)
        elif topic == 'replace blockchain':
            body_string = bytes.decode(body)
            body_dict = json.loads(body_string)
            chain_index = body_dict['index']
            block_list = body_dict['blocks']
            i = 0
            for index in range(chain_index - 1, len(self.blockchain.chain)):
                self.blockchain.chain[index - 1] = block_list[i]
                i += 1
        # asyncio.ensure_future(self.handle())

    def send_message(self, message, values):
        """

        :param message: message to send
        :param values: product information
        """
        context = zmq.Context.instance()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://{}:{}'.format(SERVER, WRITE_PORT))
        message_bytes = str.encode(message)
        values_string = json.dumps(values)
        values_bytes = str.encode(values_string, encoding='utf-8')
        socket.send_multipart([message_bytes, values_bytes])
        # self.start()
        ret = socket.recv()
        print(ret)
        self.handle()

    def start(self):
        self.loop.create_task(self.handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.zmqSubSocket.close()
        self.zmqContext.destroy()
