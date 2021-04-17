import socket
import time
import math
import random
from _thread import *
import _pickle as pickle
import logging
import logging.config

# creating sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# creating logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('server.py')

# constants
HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5555
BALL_RADIUS = 5
START_RADIUS = 7

ROUND_TIME = 5 * 60
MASS_LOSS_TIME = 6

WIDTH, HEIGHT = 1600, 830

# connecting to server
try:
    S.bind((IP, PORT))
except socket.error as err:
    logger.error(f"{str(err)}, could not start")
    quit()

S.listen()
logger.info(f"running with local ip {IP}")

# dynamic variables
# TODO: list of colors
players = {}
balls = []
connections = 0
_id = 0
colors = []
start = False
stat_time = 0
game_time = "Game will start soon"
nxt = 1


def realse_players_mass(players) -> None:
    for player in players:
        p = players[player]
        if p["score"] > 8:
            p["score"] = math.floor(p["score"]*0.9)


def with_ball_collision_checking(players, balls) -> None:
    for player in players:
        p = players[player]
        x = p['x']
        y = p['y']

        for ball in balls:
            bx = ball[0]
            by = ball[1]

            distance = math.sqrt((x - bx)**2 + (y - by)**2)
            if distance <= START_RADIUS + p["score"]:
                p["score"] += 0.5
                balls.remove(ball)


def players_collision_checking(players) -> None:
    a=5
    b=10
    pass


def create_balls(balls, n) -> None:
    pass


def start_location(players) -> tuple:
    pass


def thread_for_players(conn, _id) -> None:
    pass


