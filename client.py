import socket
import _pickle as pickle
import logging.config

# creating logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('server.py')


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "there goes your local IP"
        self.port = 5555
        self.address = (self.host, self.port)

    def connect(self, name) -> int:
        """
        Open connection between server and player.
        :param name: str, name of player
        :return: int, this will be interpreted as player's id
        """
        self.client.connect(self.address)
        self.client.send(str.encode(name))
        returned = self.client.recv(8)
        return int(returned.decode())

    def disconnect(self) -> None:
        """
        Closes connection between server and player.
        """
        self.client.close()

    def send(self, data, pick=False):
        """
        Sends data between server and player.
        :param data:
        :param pick: Always false, required argument
        :return: depends, mostly this is pack of data like balls and players
        """
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
