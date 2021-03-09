import pygame as pg

from utils import get_geo_object


class InputBox:
    def __init__(self, x, y, w, h, expansion_side, text='', color='lightskyblue3'):
        self.rect = pg.Rect(x, y, w, h)
        self.min_width = w
        self.min_x = x
        self.expansion_side = expansion_side
        self.color = pg.Color(color)
        self.text = text
        self.font = pg.font.Font(None, 24)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def text_past(self, text):
        self.text = text
        self.txt_surface = self.font.render(self.text, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pg.Color('dodgerblue2') if self.active else pg.Color('lightskyblue3')
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN and self.text != '':
                    toponym = get_geo_object(self.text)
                    return toponym
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.update(True)
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def clear(self):
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.rect.x = self.min_x
        self.rect.w = self.min_width

    def update(self, backspace=False):
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        if self.rect.w < width:
            if self.expansion_side == 'left':
                self.rect.x -= width - self.rect.w
            self.rect.w = width
        elif backspace and self.rect.w > self.min_width and self.text:
            step = self.txt_surface.get_width() // len(self.text)
            self.rect.x = self.rect.x + step if self.rect.x <= self.min_x else self.rect.x
            self.rect.w -= step

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)
