import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, text: str, pos: tuple, size: tuple, group: pg.sprite.AbstractGroup):
        super(Button, self).__init__(group)
        self.x, self.y = pos
        self.width, self.height = size
        self.text = text
        self.color = 'black'
        self.image = None
        pg.font.init()
        self.draw()
        self.texts = ['схема', 'спутник']
        self.translate = {
            'схема': 'map',
            'спутник': 'sat',
        }

    def switch_text(self):
        self.text = self.texts[(self.texts.index(self.text) + 1) % len(self.texts)]

    def change_text(self, text: str):
        self.text = text
        self.draw()

    def get_text(self) -> str:
        return self.translate[self.text]

    def draw(self):
        font = pg.font.SysFont('Consolas', 24)
        text = font.render(self.text, True, pg.Color(self.color))
        self.image = text
        self.rect = pg.Rect((self.x, self.y, self.width, self.height))

    def handle_click(self, pos: tuple):
        x1, y1 = pos
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        return False
