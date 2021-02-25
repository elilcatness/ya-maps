import pygame as pg

from utils import get_image, extract_coords, get_toponym_scale
from button import Button
from textinput import InputBox


def main():
    coords = [43.574330, 43.389149]
    zoom = 2
    map_type = 'map'
    img = pg.image.load(get_image(coords, map_type, zoom))
    pg.init()
    all_sprites = pg.sprite.Group()
    screen = pg.display.set_mode((600, 450))
    inputbox = InputBox(395, 0, 140, 32)
    button = Button('схема', (0, 0), (100, 100), all_sprites)
    map_type = button.get_text()
    screen.blit(img, (0, 0))
    running = True
    clock = pg.time.Clock()
    fps = 60
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN):
                    adjustable_sizes = [(range(0, 7), 10 / zoom), (range(7, 10), 1 / zoom),
                                        (range(10, 14), 0.1 / zoom), (range(14, 18), 0.01 / zoom),
                                        (range(18, 20), 0.005 / zoom)]
                    adjust = list(filter(lambda x: zoom in x[0], adjustable_sizes))[0][1]
                    translate = {pg.K_LEFT: (-1 * adjust, 0), pg.K_RIGHT: (1 * adjust, 0),
                                 pg.K_UP: (0, 1 * adjust), pg.K_DOWN: (0, -1 * adjust)}
                    options = translate[event.key]
                    for i in range(len(options)):
                        coords[i] += options[i]
                    img = pg.image.load(get_image(coords, map_type, zoom))
                elif event.key == pg.K_PAGEUP:
                    if zoom < 19:
                        zoom += 1
                        img = pg.image.load(get_image(coords, map_type, zoom))
                elif event.key == pg.K_PAGEDOWN:
                    if zoom > 2:
                        zoom -= 1
                        img = pg.image.load(get_image(coords, map_type, zoom))
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.handle_click(event.pos):
                    button.switch_text()
                    button.draw()
                    map_type = button.get_text()
                    img = pg.image.load(get_image(coords, map_type, zoom))
            request = inputbox.handle_event(event)
            if request and isinstance(request, dict):
                toponym = request
                coords = extract_coords(toponym)
                mark = {'coords': ','.join(map(str, coords)),
                        'type': 'pm2',
                        'color': 'rd',
                        'size': 'm'}
                size = get_toponym_scale(toponym)
                img = pg.image.load(get_image(coords, map_type, size=size, mark=mark))
        screen.blit(img, (0, 0))
        all_sprites.draw(screen)
        inputbox.update()
        inputbox.draw(screen)
        pg.display.flip()
        clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()
