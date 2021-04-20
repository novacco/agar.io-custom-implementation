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


WIN = pg.display.set_mode((WIDTH, HEIGHT))
