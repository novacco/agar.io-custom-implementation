import pygame as pg
import sys

pg.init()

NAME_FONT = pg.font.SysFont("Arial", 20)
PROMPT_FONT = pg.font.SysFont("Arial", 40)

clock = pg.time.Clock()


def login_window():
    """
    creates a pop up window asking player for a name
    :return:
    """
    LOGIN = pg.display.set_mode((300, 200))
    name = ''

    rect = pg.Rect(50, 100, 200, 32)
    connect_button = pg.Rect(100, 150, 100, 32)

    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                        return name
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pg.K_ESCAPE or event.type == pg.QUIT:
                    pg.display.quit()
                    pg.quit()
                    sys.exit()
                else:
                    name += event.unicode
            if event.type == pg.MOUSEBUTTONDOWN:
                if 100 <= pg.mouse.get_pos()[0] <= 200 and 150 <= pg.mouse.get_pos()[1] <= 182:
                    return name
        LOGIN.fill((189, 189, 189))
        pg.draw.rect(LOGIN, pg.Color('white'), rect, 2)
        pg.draw.rect(LOGIN, pg.Color("Black"), connect_button, 2)
        button_text = NAME_FONT.render("Connect", True, (0, 0, 0))
        LOGIN.blit(button_text, (120, 155))
        prompt_surface = PROMPT_FONT.render("What's your name?", True, (0, 0, 0,))
        LOGIN.blit(prompt_surface, (11, 0))
        text_surface = NAME_FONT.render(name, True, (0, 0, 0))
        LOGIN.blit(text_surface, (rect.x + 5, rect.y + 5))
        rect.w = max(text_surface.get_width() + 10, 200)
        pg.display.flip()
        clock.tick(60)
