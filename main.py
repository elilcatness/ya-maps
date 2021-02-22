import os
import sys
import pygame
import requests


def main():
    basic = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(basic, params={'ll': '43.574330,43.389149',
                                           'z': 2,
                                           'l': 'map'})
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    while pygame.event.wait().type != pygame.QUIT:
        pass
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()
