import pygame
import os
import sys

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
borders = pygame.sprite.Group()
ships = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

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
            self.image = pygame.transform.scale(load_image('white_border.PNG'), (1, y2 - y1))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.add(borders)
            self.image = pygame.transform.scale(load_image('white_border.PNG'), (x2 - x1, 1))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(ships)
        self.image = pygame.transform.scale(load_image('spaceship.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 25
        self.rect.y = height // 2 - 25

    def update(self, direction):
        game_area = pygame.Rect(6, 6, width - 51, height - 121)

        if game_area.collidepoint(self.rect.x, self.rect.y):
            if direction == 'left':
                self.rect.x -= 1
            elif direction == 'right':
                self.rect.x += 1
            elif direction == 'up':
                self.rect.y -= 1
            elif direction == 'down':
                self.rect.y += 1
        else:
            if pygame.sprite.spritecollideany(self, vertical_borders):
                if self.rect.x < width // 2:
                    self.rect.x += 1
                elif self.rect.x > width // 2:
                    self.rect.x -= 1
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                if self.rect.y < height // 2:
                    self.rect.y += 1
                elif self.rect.y > height // 2:
                    self.rect.y -= 1


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__(all_sprites)
        self.add(player_bullets)
        self.image = pygame.transform.scale(load_image('player_bullet.png', colorkey=-1), (5, 20))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        if pygame.sprite.spritecollideany(self, borders):
            self.kill()
        else:
            self.rect.y -= 3


def intro():
    img = pygame.transform.scale(load_image('fon_intro.jpg'), (600, 400))

    intro_font = pygame.font.Font(None, 75)
    intro_text = intro_font.render('Galaktischer Blitzkrieg', True, pygame.Color('#ffffff'))

    screen.fill(pygame.Color('#000000'))

    screen.blit(img, (0, 0))
    screen.blit(intro_text, (3, 175))

    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False


def main_menu():
    lev1_button_rect = pygame.Rect(50, 50, 100, 50)
    lev1_font = pygame.font.Font(None, 60)
    lev1_text = lev1_font.render('1', True, pygame.Color('#ffffff'))
    lev1_button_color = pygame.Color('#1E90FF')

    screen.fill(pygame.Color('#000000'))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        if lev1_button_rect.collidepoint(pygame.mouse.get_pos()):
            lev1_button_color = pygame.Color('#FF0000')
            if pygame.mouse.get_pressed()[0]:
                level1()
        else:
            lev1_button_color = pygame.Color('#1E90FF')

        pygame.draw.rect(screen, lev1_button_color, lev1_button_rect)
        screen.blit(lev1_text, (90, 55))
        pygame.display.flip()


def level1():
    Border(5, 5, width - 5, 5)
    Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PlayerBullet(spaceship.rect.x + 20, spaceship.rect.y - 20)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            spaceship.update('down')

        player_bullets.update()

        screen.fill(pygame.Color('#000000'))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)

        pygame.display.flip()
        clock.tick(120)


if __name__ == '__main__':
    intro()
    main_menu()
