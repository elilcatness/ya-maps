import pygame as pg

from utils import get_geo_object


class InputBox:
    def __init__(self, x, y, w, h, text='', color='lightskyblue3'):
        self.rect = pg.Rect(x, y, w, h)
        self.width = w
        self.min_width = w
        self.min_x = x
        self.color = pg.Color('lightskyblue3')
        self.color = pg.Color(color)
        self.text = text
        self.font = pg.font.Font(None, 32)
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
                    self.text = ''
                    return toponym
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def clear(self):
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.rect.x = self.min_x
        self.rect.w = self.min_width
        self.width = self.min_width

    def update(self, backspace=False):
        width = max(self.width, self.txt_surface.get_width() + 10)
        if self.width < width:
            self.rect.x -= width - self.width
        elif backspace and self.width > self.min_width:
            if self.rect.x <= self.min_x:
                self.rect.x += self.txt_surface.get_width() // len(self.text)
            self.width -= 10
            # self.rect.x += self.width - self.min_width
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)
