import sys
import pygame as pg
from io import BytesIO
import requests


def get_image(coords: list, scale: int):
    basic = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(basic, params={'ll': ','.join(map(str, coords)),
                                           'z': scale,
                                           'l': 'map'})
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return BytesIO(response.content)


def main():
    coords = [43.574330, 43.389149]
    zoom = 2
    img = pg.image.load(get_image(coords, zoom))
    pg.init()
    screen = pg.display.set_mode((600, 450))
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
                    img = pg.image.load(get_image(coords, zoom))
                elif event.key == pg.K_PAGEUP:
                    if zoom < 22:
                        zoom += 1
                    img = pg.image.load(get_image(coords, zoom))
                elif event.key == pg.K_PAGEDOWN:
                    if zoom > 2:
                        zoom -= 1
                    img = pg.image.load(get_image(coords, zoom))
        screen.blit(img, (0, 0))
        pg.display.flip()
        clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()
