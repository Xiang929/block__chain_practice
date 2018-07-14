from app import app
from app.mod_goods.GoodsController import subscriber
import threading
import signal
import sys


def task():
    subscriber.handle()


def my_quit(signum, frame):
    print('You choose Ctrl + C to end the program.')
    sys.exit()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    signal.signal(signal.SIGINT, my_quit)
    signal.signal(signal.SIGTERM, my_quit)
    handle_task = threading.Thread(target=task)
    handle_task.setDaemon(True)
    handle_task.start()

    app.run(host='127.0.0.1', port=port, use_reloader=False,debug=True)
