import os

import pygame as pg

from button import Button
from textinput import InputBox
from utils import get_image, extract_coords, get_toponym_scale


def main():
    params = {'coords': [43.574330, 43.389149], 'z': 2, 'map_type': 'map'}
    img = pg.image.load(get_image(params))
    pg.init()
    all_sprites = pg.sprite.Group()
    screen = pg.display.set_mode((600, 450))
    pg.display.set_caption('Яндекс.Карты')
    pg.display.set_icon(pg.image.load(os.path.join('data', 'img', 'yandex.png')))
    inputbox = InputBox(370, 5, 225, 24, 'left')
    inputbox_all_adress = InputBox(5, 420, 225, 24, 'right', '', 'dodgerblue2')
    button = Button('Схема', (0, 0), (100, 100), all_sprites)
    map_type = button.get_text()
    screen.blit(img, (0, 0))
    running = True
    clock = pg.time.Clock()
    fps = 60
    inputboxs = [inputbox, inputbox_all_adress]
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN):
                    adjustable_sizes = [(range(0, 7), 10 / params['z']), (range(7, 10), 1 / params['z']),
                                        (range(10, 14), 0.1 / params['z']), (range(14, 18), 0.01 / params['z']),
                                        (range(18, 20), 0.005 / params['z'])]
                    adjust = list(filter(lambda x: params['z'] in x[0], adjustable_sizes))[0][1]
                    translate = {pg.K_LEFT: (-1 * adjust, 0), pg.K_RIGHT: (1 * adjust, 0),
                                 pg.K_UP: (0, 1 * adjust), pg.K_DOWN: (0, -1 * adjust)}
                    options = translate[event.key]
                    for i in range(len(options)):
                        params['coords'][i] += options[i]
                    img = pg.image.load(get_image(params))
                elif event.key == pg.K_PAGEUP:
                    if params['z'] < 19:
                        params['z'] += 1
                        img = pg.image.load(get_image(params))
                elif event.key == pg.K_PAGEDOWN:
                    if params['z'] > 2:
                        params['z'] -= 1
                        img = pg.image.load(get_image(params))
            if event.type == pg.MOUSEBUTTONDOWN:
                if button.handle_click(event.pos):
                    button.switch_text()
                    button.draw()
                    params['map_type'] = button.get_text()
                    img = pg.image.load(get_image(params))
            request = inputbox.handle_event(event)
            if request and isinstance(request, dict):
                toponym = request
                inputbox_all_adress.text_past(toponym['metaDataProperty']['GeocoderMetaData']['text'])
                params['coords'] = extract_coords(toponym)
                params['mark'] = {'coords': ','.join(map(str, params['coords'])),
                                  'type': 'pm2',
                                  'color': 'rd',
                                  'size': 'm'}
                params['z'] = get_toponym_scale(toponym)
                img = pg.image.load(get_image(params))
        screen.blit(img, (0, 0))
        all_sprites.draw(screen)
        for inp in inputboxs:
            inp.update()
            inp.draw(screen)
        pg.display.flip()
        clock.tick(fps)
    pg.quit()


if __name__ == '__main__':
    main()
