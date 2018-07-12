import zmq


class Publisher(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def publiser_run_tasks(self):
        context = zmq.Context.instance()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://{}:{}'.format(self.host, self.port))

        while True:
            [topic, content] = socket.recv_multipart()
            if topic == b'new block':
                socket.send_multipart([topic, content])
            elif topic == b'new block finished':
                socket.send_multipart([b'creat block', content])
            elif topic == b'modify block':
                socket.send_multipart([topic, content])
            elif topic == b'modify block finished':
                pass
