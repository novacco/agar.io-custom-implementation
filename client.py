import socket
import _pickle as pickle
import logging.config

# creating logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('server.py')


# TODO: descirption of class and functions inside

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "172.104.158.199"
        self.port = 5555
        self.address = (self.host, self.port)

    def connect(self, name) -> int:
        self.client.connect(self.address)
        self.client.send(str.encode(name))
        returned = self.client.recv(8)
        return int(returned.decode())

    def disconnect(self) -> None:
        self.client.close()

    def send(self, data, pick=False) -> str:
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048 * 4)
            try:
                reply = pickle.loads(reply)
            except Exception as exc:
                logger.exception(exc)
            return reply
        except socket.error as err:
            logger.error(err)
