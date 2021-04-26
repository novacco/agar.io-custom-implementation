import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pg
from client import Network
import os
import random
import datetime
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('game.py')

pg.font.init()

PLAYER_RADIUS = 10
BALL_RADIUS = 5
START_VELOCITY = 10
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255),
          (0, 128, 255), (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128), (128, 128, 128),
          (0, 0, 0)]
WIDTH, HEIGHT = 1600, 830

NAME_FONT = pg.font.SysFont("Arial", 20)
TIME_FONT = pg.font.SysFont("Arial", 30)
SCORE_FONT = pg.font.SysFont("Arial", 25)
FONT_COLOR = (0, 0, 0)

players = {}
balls = []


def convert_time(time):
    if type(time) is not int:
        logger.error(f"type of time must be INT, returning error")
        return "ERR"
    return str(datetime.timedelta(seconds=time))


def redraw_window(players, balls, game_time, score):
    WIN.fill((255, 255, 255))

    for ball in balls:
        pg.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)

    for player in sorted(players, key=lambda x: players[x]["score"]):
        p = players[player]
        pg.draw.circle(WIN, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + round(p["score"]))
        name = NAME_FONT.render(p["name"], True, FONT_COLOR)
        WIN.blit(name, (p["x"] - name.get_width() / 2, p["y"] - name.get_width() / 2))

    sorted_players = list(reversed(sorted(players, key=lambda x: players[x]["score"])))
    scoreboard = TIME_FONT.render("Scoreboard", True, FONT_COLOR)
    start_y = 25
    x = WIDTH - scoreboard.get_width() - 10
    WIN.blit(scoreboard, (x, 5))
    top3 = min(len(players), 3)
    for place, x in enumerate(sorted_players[:top3]):
        player = SCORE_FONT.render(f'{place + 1}. {players[x]["name"]} - {players[x]["score"]}', True, FONT_COLOR)
        WIN.blit(player, (x, start_y + place * 20))

    time = TIME_FONT.render(f'Time: {convert_time(game_time)}', True, FONT_COLOR)
    WIN.blit(time, (10, 10))

    scr = TIME_FONT.render(f'Score: {round(score)}', True, FONT_COLOR)
    WIN.blit(scr, (10, 15 + scr.get_height()))


def game(name):
    global players

    server = Network()
    current_id = server.connect(name)
    balls, players, game_time = server.send("get")

    clock = pg.time.Clock()

    run = True
    while run:
        clock.tick(30)
        p = players[current_id]
        velocity = START_VELOCITY - round(p["score"] / 12)
        if velocity < 1:
            velocity = 1

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            if p["x"] - velocity - PLAYER_RADIUS - p["score"] >= 0:
                p["x"] -= velocity
        if keys[pg.K_d]:
            if p["x"] + velocity + PLAYER_RADIUS + p["score"] <= WIDTH:
                p["x"] += velocity
        if keys[pg.K_w]:
            if p["y"] - velocity - PLAYER_RADIUS - p["score"] >= 0:
                p["y"] -= velocity
        if keys[pg.K_s]:
            if p["y"] + velocity + PLAYER_RADIUS + p["score"] <= HEIGHT:
                p["y"] += velocity

        data = f'move {p["x"]} {p["y"]}'
        balls, players, game_time = server.send(data)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
        redraw_window(players, balls, game_time, p["score"])
        pg.display.update()

    server.disconnect()
    pg.quit()
    quit()


while True:
    name = input("Write down your nickname:")
    if 0 < len(name) < 20:
        break
    else:
        print("Nickname must be between 1 and 19 chars")


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(f"Agar.IO implementation {WIDTH}x{HEIGHT}")

game(name)
