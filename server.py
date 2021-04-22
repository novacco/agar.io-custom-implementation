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
colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255),
          (0, 128, 255), (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128), (128, 128, 128),
          (0, 0, 0)]
start = False
start_time = 0
game_time = "Game will start soon"
nxt = 1


def realse_players_mass(players) -> None:
    for player in players:
        p = players[player]
        if p["score"] > 8:
            p["score"] = math.floor(p["score"] * 0.9)


def with_ball_collision_checking(players, balls) -> None:
    for player in players:
        p = players[player]
        x = p['x']
        y = p['y']

        for ball in balls:
            bx = ball[0]
            by = ball[1]

            distance = math.sqrt((x - bx) ** 2 + (y - by) ** 2)
            if distance <= START_RADIUS + p["score"]:
                p["score"] += 0.5
                balls.remove(ball)


def players_collision_checking(players) -> None:
    sorted_players = sorted(players, key=lambda x: players[x]["score"])
    for x, p1 in enumerate(sorted_players):
        for p2 in sorted_players[x + 1:]:
            p1x = players[p1]["x"]
            p1y = players[p1]["y"]
            p2x = players[p2]["x"]
            p2y = players[p2]["y"]

            distance = math.sqrt((p1x - p2x) ** 2 + (p1y - p2y) ** 2)
            if distance < players[p2]["score"] - players[p1]["score"] * 0.8:
                score = math.sqrt(players[p2]["score"] ** 2 + players[p1]["score"] ** 2)
                logger.info(f'{players[p2]["name"]} ate {players[p1]["name"]} and gained {score} points')
                players[p2]["score"] = score
                players[p1]["score"] = 0
                players[p1]["x"], players[p1]["y"] = start_location(players)


def create_balls(balls, n) -> None:
    for x in range(n):
        while True:
            stop = True
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            for player in players:
                p = players[player]
                distance = math.sqrt((x - p["x"]) ** 2 + (y - p["y"]) ** 2)
                if distance <= START_RADIUS + p["score"]:
                    stop = False
            if stop:
                break
        balls.append((x, y, random.choice(colors)))


def start_location(players) -> tuple:
    while True:
        stop = True
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        for player in players:
            p = players[player]
            distance = math.sqrt((x - p["x"]) ** 2 + (y - p["y"]) ** 2)
            if distance <= START_RADIUS + p["score"]:
                stop = False
        if stop:
            break
    return x, y


def new_player(conn, _id) -> None:
    """

    :param conn: ip address
    :param _id: int
    """
    global connections, players, balls, game_time, nxt, start
    current_id = _id

    data = conn.recv(16)
    name = data.decode("utf-8")
    logger.info(f"{name} connected")

    logger.error(current_id)
    color = colors[current_id]
    x, y = start_location(players)
    players[current_id] = {"x": x, "y": y, "color": color, "score": 0, "name": name}

    conn.send(str.encode(str(current_id)))

    while True:
        if start:
            game_time = round(time.time() - start_time)
            if game_time >= ROUND_TIME:
                start = False
            else:
                if game_time // MASS_LOSS_TIME == nxt:
                    nxt += 1
                    realse_players_mass(players)
                    logger.info(f"{name} started playing")
        try:
            data = conn.recv(32)
            if not data:
                logger.error(f"DATA from {name} not collected")
                break

            data = data.decode("utf-8")
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players[current_id]["x"] = x
                players[current_id]["y"] = y

                if start:
                    with_ball_collision_checking(players, balls)
                    players_collision_checking(players)

                if len(balls) < 200:
                    number = random.randrange(100, 200)
                    create_balls(balls, number)
                    logger.info(f"Created {number} balls")

                send_data = pickle.dumps((balls, players, game_time))

            elif data.split(" ")[0] == "id":
                send_data = str.encode(str(current_id))
            elif data.split(" ")[0] == "jump":
                send_data = pickle.dumps((balls, players, game_time))
            else:
                send_data = pickle.dumps((balls, players, game_time))

            conn.send(send_data)

        except Exception as e:
            logger.exception(e)
            break

        time.sleep(0.001)

    logger.info(f"{name}(id = {current_id}) disconnected")
    connections -= 1
    del players[current_id]
    conn.close()


create_balls(balls, random.randrange(220, 270))

logger.info("Map has been generated")
logger.info("Waiting for connections")

while True:
    host, address = S.accept()
    logger.info(f"New connection from {address}")

    if address[0] == IP and not start:
        start = True
        start_time = time.time()
        logger.info("Host connected, game starts")

    connections += 1
    start_new_thread(new_player, (host, _id))
    _id += 1

logger.info("Server is shutting down")
