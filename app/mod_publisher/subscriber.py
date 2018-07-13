import functools
import signal

import zmq
import json
import asyncio
from zmq import asyncio

from app.mod_commodity.blockchain import Blockchain


class Subscriber(object):
    def __init__(self, host, port):
        self.loop = asyncio.get_event_loop()
        self.zmqContext = zmq.asyncio.Context()
        self.blockchain = Blockchain()
        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.zmqSubSocket.connect('tcp:////{}:{}'.format(host, port))

    async def handle(self):
        [topic, body] = await self.zmqSubSocket.recv_multipart()
        if topic == b'new block':
            transactions_string = bytes.decode(body)
            transactions = json.loads(transactions_string)
            new_block = await self.blockchain.new_block(transactions)
            new_block_string = json.dumps(new_block)
            self.zmqSubSocket.send_multipart([b'new block finished',
                                              bytes(new_block_string, encoding='utf-8')])
        elif topic == b'creat block':
            block_string = bytes.decode(body)
            block_obj = json.loads(block_string)
            self.blockchain.add_block(block_obj)
        elif topic == b'modify block':
            transactions_string = bytes.decode(body)
            transactions = json.loads(transactions_string)
            modify_dict = self.blockchain.modify_block(transactions)
            modify_string = json.dumps(modify_dict)
            self.zmqSubSocket.send_multipart([b'modify block finished',
                                              bytes(modify_string, encoding='utf-8')])
        elif topic == b'modify new blockchain':
            body_string = bytes.decode(body)
            body_dict = json.loads(body_string)
            chain_index = body_dict['index']
            block_list = body_dict['blocks']
            i = 0
            for index in range(chain_index - 1, len(self.blockchain.chain)):
                self.blockchain.chain[index - 1] = block_list[i]
                i += 1
        asyncio.ensure_future(self.handle())

    def send_message(self, message, values):
        """

        :param message: message to send
        :param values: product information
        """
        message_bytes = str.encode(message)
        values_string = json.dumps(values)
        values_bytes = str.encode(values_string)
        self.zmqSubSocket.send_multipart([message_bytes, values_bytes])

    def start(self):
        for signame in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(getattr(signal, signame),
                                         functools.partial(self.stop, signame))
        self.loop.create_task(self.handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.zmqSubSocket.close()
        self.zmqContext.destroy()
