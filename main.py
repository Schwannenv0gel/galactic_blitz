import pygame
import os
import sys


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
borders = pygame.sprite.Group()
ships = pygame.sprite.Group()
enemies = pygame.sprite.Group()

pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join(r'data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.add(borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.add(borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__(all_sprites)
        self.add(ships)
        self.image = pygame.transform.scale(load_image('spaceship.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self, move_x, move_y):
        if pygame.sprite.spritecollideany(self, vertical_borders) or not pygame.mouse.get_focused():
            if pygame.mouse.get_pos()[1] < height // 2:
                self.rect.y += abs(pygame.mouse.get_pos()[1])
            if pygame.mouse.get_pos()[1] > height // 2:
                self.rect.y = height - 30
        elif pygame.sprite.spritecollideany(self, horizontal_borders) or not pygame.mouse.get_focused():
            if pygame.mouse.get_pos()[0] < width // 2:
                self.rect.x = 5
            else:
                self.rect.x = width - 50
        else:
            self.rect.x = move_x
            self.rect.y = move_y


if __name__ == '__main__':

    screen.fill(pygame.Color('#ffffff'))

    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)

    sh_x = width // 2 - 25
    sh_y = height // 2 - 25
    spaceship = SpaceShip(sh_x, sh_y)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                spaceship.update(event.pos[0] - 25, event.pos[1] - 25)

        screen.fill(pygame.Color('#ffffff'))

        borders.draw(screen)
        ships.draw(screen)

        pygame.display.flip()
