import os
import sys
from io import BytesIO
import pygame as pg
import requests

from button import Button


def get_image(coords, scale: int, map_type: str):
    basic = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(basic, params={'ll': ','.join(map(str, coords)),
                                           'z': scale,
                                           'l': 'sat'})
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return BytesIO(response.content)


def main():
    coords = [43.574330, 43.389149]
    zoom = 2
    map_type = 'map'
    img = pg.image.load(get_image(coords, zoom, map_type))
    pg.init()
    all_sprites = pg.sprite.Group()
    screen = pg.display.set_mode((600, 450))
    screen.blit(img, (0, 0))
    button = Button('схема', (0, 0), (100, 100), all_sprites)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    coords[0] -= 2
                elif event.key == pg.K_RIGHT:
                    coords[0] += 2
                elif event.key == pg.K_UP:
                    coords[1] += 2
                elif event.key == pg.K_DOWN:
                    coords[1] -= 2
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.handle_click(event.pos):
                    button.switch_text()
                    button.draw()
                    img = pg.image.load(get_image(coords, zoom, button.get_text()))
        img = pg.image.load(get_image(coords, zoom, map_type))
        screen.blit(img, (0, 0))
        all_sprites.draw(screen)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
