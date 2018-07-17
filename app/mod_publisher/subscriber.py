import json
import multiprocessing
import queue

import zmq

from app.mod_commodity.blockchain import Blockchain
from app.mod_goods import GoodsController
from config import *

topics_new_block = queue.Queue(100)
topics_finished = queue.Queue(100)
add = False


class Subscriber(object):
    def __init__(self, host, port):
        self.block_chain = Blockchain()
        self.host = host
        self.flag = False
        self.port = port

    def handle(self):
        global task
        global topics_new_block
        global topics_finished
        global finished
        global add
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        socket.connect("tcp://%s:%s" % (self.host, self.port))
        print("START")
        while True:
            if (topics_new_block.empty() is False and add is False) or topics_finished.empty() is False:
                if add is False:
                    [topic, body] = topics_new_block.get()
                else:
                    [topic, body] = topics_finished.get()
                if topic == b'new block':
                    add = True
                    self.flag = False
                    GoodsController.new_flag = False
                    transactions_string = bytes.decode(body)
                    transactions = json.loads(transactions_string)
                    task = multiprocessing.Process(target=self.send_result,
                                                   args=('new block finished', transactions,))
                    task.start()
                elif topic == b'create block':
                    add = False
                    self.flag = True
                    GoodsController.new_flag = True
                    task.terminate()
                    block_string = bytes.decode(body)
                    block_obj = json.loads(block_string)
                    self.block_chain.add_block(block_obj)
                elif topic == b'modify block':
                    transactions_string = bytes.decode(body)
                    transactions = json.loads(transactions_string)
                    task = multiprocessing.Process(target=self.send_result,
                                                   args=('modify block finished', transactions,))
                elif topic == 'replace blockchain':
                    body_string = bytes.decode(body)
                    body_dict = json.loads(body_string)
                    chain_index = body_dict['index']
                    block_list = body_dict['blocks']
                    i = 0
                    for index in range(chain_index - 1, len(self.block_chain.chain)):
                        self.block_chain.chain[index - 1] = block_list[i]
                        i += 1
            else:
                if add is True:
                    while True:
                        [topic, body] = socket.recv_multipart()
                        if b'create' in topic:
                            topics_finished.put([topic, body])
                            break
                        else:
                            topics_new_block.put([topic, body])
                else:
                    [topic, body] = socket.recv_multipart()
                    topics_new_block.put([topic, body])
                print(topic, body)

    def send_message(self, message, values=None, synchronization=False):
        """
        :param synchronization: type of operation
        :param message: message to send
        :param values: product information
        :type message: str
        :type values: dict
        """
        context = zmq.Context.instance()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://{}:{}'.format(SERVER, WRITE_PORT))
        message_bytes = str.encode(message)
        values_string = json.dumps(values)
        values_bytes = str.encode(values_string, encoding='utf-8')
        socket.send_multipart([message_bytes, values_bytes])
        if synchronization is True:
            self.block_chain.chain = socket.recv_pyobj()
            if len(self.block_chain.chain) > 0:
                print('Synchronization information succeeded')
        else:
            ret = socket.recv()
            print(ret)

    def send_result(self, message, transactions):
        """
        :type message: str
        :type transactions: dict
        """
        new_block = self.block_chain.new_block(transactions)
        if self.flag is False:
            self.send_message(message, new_block)

    def synchronizing(self):
        self.send_message('synchronizing information', synchronization=True)
