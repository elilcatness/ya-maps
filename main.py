import sys
import pygame as pg
from io import BytesIO
import requests

from button import Button


def get_image(coords, scale: int, map_type: str):
    basic = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(basic, params={'ll': ','.join(map(str, coords)),
                                           'z': scale,
                                           'l': map_type})
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
    clock = pg.time.Clock()
    fps = 60
    while running:
        screen.fill('black')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN):
                    translate = {pg.K_LEFT: (-2, 0), pg.K_RIGHT: (2, 0),
                                 pg.K_UP: (0, 2), pg.K_DOWN: (0, -2)}
                    options = translate[event.key]
                    for i in range(len(options)):
                        coords[i] += options[i]
                    img = pg.image.load(get_image(coords, zoom, button.get_text()))
                elif event.key == pg.K_PAGEUP:
                    if zoom < 22:
                        zoom += 1
                        img = pg.image.load(get_image(coords, zoom, button.get_text()))
                elif event.key == pg.K_PAGEDOWN:
                    if zoom > 2:
                        zoom -= 1
                        img = pg.image.load(get_image(coords, zoom, button.get_text()))
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.handle_click(event.pos):
                    button.switch_text()
                    button.draw()
                    img = pg.image.load(get_image(coords, zoom, button.get_text()))
        img = pg.image.load(get_image(coords, zoom, map_type))
        screen.blit(img, (0, 0))
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()
