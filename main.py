import pygame
import os
import sys
import csv

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
borders = pygame.sprite.Group()
ships = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

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


def load_level(filename):
    pass


def enemy_appear():
    pass


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
        self.image = pygame.transform.scale(load_image('spaceship.png', colorkey=-1), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 25
        self.rect.y = height // 2 + 55
        self.hp = 3
        self.damage_multipler = 1

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


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, bonus_type=None):
        super().__init__(all_sprites)
        self.add(enemies)
        self.hp = 5
        self.bonus_type = bonus_type
        self.image = pygame.transform.scale(load_image('enemy1.png', colorkey=-1), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        if pygame.sprite.spritecollideany(self, player_bullets):
            self.hp -= pygame.sprite.spritecollideany(self, player_bullets).damage
        if self.hp == 0:
            if self.bonus_type == 'life':
                LifeBonus(self.rect.x + 12, self.rect.y + 12)
            elif self.bonus_type == 'damage':
                DamageBonus(self.rect.x + 12, self.rect.y + 12)
            self.kill()
        self.rect.y += 1


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, bonus_type=None):
        super().__init__(all_sprites)
        self.add(enemies)
        self.hp = 10
        self.bonus_type = bonus_type
        self.image = pygame.transform.scale(load_image('enemy2.png', colorkey=-1), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        if pygame.sprite.spritecollideany(self, player_bullets):
            self.hp -= pygame.sprite.spritecollideany(self, player_bullets).damage
        if self.hp == 0:
            if self.bonus_type == 'life':
                LifeBonus(self.rect.x + 12, self.rect.y + 12)
            elif self.bonus_type == 'damage':
                DamageBonus(self.rect.x + 12, self.rect.y + 12)
            self.kill()
        self.rect.y += 1


class Enemy3(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, bonus_type=None):
        super().__init__(all_sprites)
        self.add(enemies)
        self.hp = 15
        self.bonus_type = bonus_type
        self.image = pygame.transform.scale(load_image('enemy3.png', colorkey=-1), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        if pygame.sprite.spritecollideany(self, player_bullets):
            self.hp -= pygame.sprite.spritecollideany(self, player_bullets).damage
        if self.hp == 0:
            if self.bonus_type == 'life':
                LifeBonus(self.rect.x + 12, self.rect.y + 12)
            elif self.bonus_type == 'damage':
                DamageBonus(self.rect.x + 12, self.rect.y + 12)
            self.kill()
        self.rect.y += 1


class LifeBonus(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__(all_sprites)
        self.add(bonuses)
        self.image = pygame.transform.scale(load_image('life_bonus.png', colorkey=-1), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.rect.y > height // 2:
                self.kill()
        if pygame.sprite.spritecollideany(self, ships):
            pygame.sprite.spritecollideany(self, ships).hp += 1
            self.kill()


class DamageBonus(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__(all_sprites)
        self.add(bonuses)
        self.image = pygame.transform.scale(load_image('damage_bonus.png', colorkey=-1), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def update(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.rect.y > height // 2:
                self.kill()
        if pygame.sprite.spritecollideany(self, ships):
            pygame.sprite.spritecollideany(self, ships).damage_multipler += 1
            self.kill()


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, damage_boost=1):
        super().__init__(all_sprites)
        self.add(player_bullets)
        self.image = pygame.transform.scale(load_image('player_bullet.png', colorkey=-1), (5, 20))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.damage = 1 * damage_boost

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

    lev2_button_rect = pygame.Rect(250, 50, 100, 50)
    lev2_font = pygame.font.Font(None, 60)
    lev2_text = lev2_font.render('2', True, pygame.Color('#ffffff'))
    lev2_button_color = pygame.Color('#1E90FF')

    lev3_button_rect = pygame.Rect(450, 50, 100, 50)
    lev3_font = pygame.font.Font(None, 60)
    lev3_text = lev3_font.render('3', True, pygame.Color('#ffffff'))
    lev3_button_color = pygame.Color('#1E90FF')

    lev4_button_rect = pygame.Rect(50, 200, 100, 50)
    lev4_font = pygame.font.Font(None, 60)
    lev4_text = lev4_font.render('4', True, pygame.Color('#ffffff'))
    lev4_button_color = pygame.Color('#1E90FF')

    lev5_button_rect = pygame.Rect(250, 200, 100, 50)
    lev5_font = pygame.font.Font(None, 60)
    lev5_text = lev5_font.render('5', True, pygame.Color('#ffffff'))
    lev5_button_color = pygame.Color('#1E90FF')

    lev6_button_rect = pygame.Rect(450, 200, 100, 50)
    lev6_font = pygame.font.Font(None, 60)
    lev6_text = lev6_font.render('6', True, pygame.Color('#ffffff'))
    lev6_button_color = pygame.Color('#1E90FF')

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

        if lev2_button_rect.collidepoint(pygame.mouse.get_pos()):
            lev2_button_color = pygame.Color('#FF0000')
            if pygame.mouse.get_pressed()[0]:
                level2()
        else:
            lev2_button_color = pygame.Color('#1E90FF')

        if lev3_button_rect.collidepoint(pygame.mouse.get_pos()):
            lev3_button_color = pygame.Color('#FF0000')
            if pygame.mouse.get_pressed()[0]:
                level3()
        else:
            lev3_button_color = pygame.Color('#1E90FF')

        if lev4_button_rect.collidepoint(pygame.mouse.get_pos()):
            lev4_button_color = pygame.Color('#FF0000')
            if pygame.mouse.get_pressed()[0]:
                level4()
        else:
            lev4_button_color = pygame.Color('#1E90FF')

        if lev5_button_rect.collidepoint(pygame.mouse.get_pos()):
            lev5_button_color = pygame.Color('#FF0000')
            if pygame.mouse.get_pressed()[0]:
                level5()
        else:
            lev5_button_color = pygame.Color('#1E90FF')

        if lev6_button_rect.collidepoint(pygame.mouse.get_pos()):
            lev6_button_color = pygame.Color('#FF0000')
            if pygame.mouse.get_pressed()[0]:
                level6()
        else:
            lev6_button_color = pygame.Color('#1E90FF')

        screen.fill(pygame.Color('#000000'))

        pygame.draw.rect(screen, lev1_button_color, lev1_button_rect)
        screen.blit(lev1_text, (90, 55))

        pygame.draw.rect(screen, lev2_button_color, lev2_button_rect)
        screen.blit(lev2_text, (290, 55))

        pygame.draw.rect(screen, lev3_button_color, lev3_button_rect)
        screen.blit(lev3_text, (490, 55))

        pygame.draw.rect(screen, lev4_button_color, lev4_button_rect)
        screen.blit(lev4_text, (90, 205))

        pygame.draw.rect(screen, lev5_button_color, lev5_button_rect)
        screen.blit(lev5_text, (290, 205))

        pygame.draw.rect(screen, lev6_button_color, lev6_button_rect)
        screen.blit(lev6_text, (490, 205))

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
                    PlayerBullet(spaceship.rect.x + 10, spaceship.rect.y - 5)
                    PlayerBullet(spaceship.rect.x + 36, spaceship.rect.y - 5)
                if event.key == pygame.K_BACKSPACE:
                    running = False

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


def level2():
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
                    PlayerBullet(spaceship.rect.x + 10, spaceship.rect.y - 5)
                    PlayerBullet(spaceship.rect.x + 36, spaceship.rect.y - 5)
                if event.key == pygame.K_BACKSPACE:
                    running = False

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


def level3():
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
                    PlayerBullet(spaceship.rect.x + 10, spaceship.rect.y - 5)
                    PlayerBullet(spaceship.rect.x + 36, spaceship.rect.y - 5)
                if event.key == pygame.K_BACKSPACE:
                    running = False

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


def level4():
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
                    PlayerBullet(spaceship.rect.x + 10, spaceship.rect.y - 5)
                    PlayerBullet(spaceship.rect.x + 36, spaceship.rect.y - 5)
                if event.key == pygame.K_BACKSPACE:
                    running = False

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


def level5():
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
                    PlayerBullet(spaceship.rect.x + 10, spaceship.rect.y - 5)
                    PlayerBullet(spaceship.rect.x + 36, spaceship.rect.y - 5)
                if event.key == pygame.K_BACKSPACE:
                    running = False

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


def level6():
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
                    PlayerBullet(spaceship.rect.x + 10, spaceship.rect.y - 5)
                    PlayerBullet(spaceship.rect.x + 36, spaceship.rect.y - 5)
                if event.key == pygame.K_BACKSPACE:
                    running = False

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


def final_window():
    pass


if __name__ == '__main__':
    intro()
    main_menu()
