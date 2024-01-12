import pygame
import os
import sys
import csv
import random

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
borders = pygame.sprite.Group()
ships = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
particles = pygame.sprite.Group()

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
    filename = r"data/" + filename
    with open(filename, encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        lev_map = list(reader)
        if lev_map[0][0][0] not in ['.', '1', '2', '3', '1l', '2l', '3l', '1d', '2d', '3d']:
            lev_map[0][0] = lev_map[0][0][-1]
        return lev_map


def enemy_appear(code):
    for i in range(len(code)):
        if code[i] == '1':
            Enemy1(i * 50, 6)
        elif code[i] == '2':
            Enemy2(i * 50, 6)
        elif code[i] == '3':
            Enemy3(i * 50, 6)
        elif code[i] == '1l':
            Enemy1(i * 50, 6, 'life')
        elif code[i] == '2l':
            Enemy2(i * 50, 6, 'life')
        elif code[i] == '3l':
            Enemy3(i * 50, 6, 'life')
        elif code[i] == '1d':
            Enemy1(i * 50, 6, 'damage')
        elif code[i] == '2d':
            Enemy2(i * 50, 6, 'damage')
        elif code[i] == '3d':
            Enemy3(i * 50, 6, 'damage')


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
        self.basehp = 9
        self.damage_multipler = 1

    def update(self, direction):
        game_area = pygame.Rect(6, 6, width - 51, height - 121)

        if game_area.collidepoint(self.rect.x, self.rect.y):
            if direction == 'left':
                self.rect.x -= 3
            elif direction == 'right':
                self.rect.x += 3
            elif direction == 'up':
                self.rect.y -= 3
            elif direction == 'down':
                self.rect.y += 3
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
        if self.hp == 0 or pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.bonus_type == 'life':
                LifeBonus(self.rect.x + 12, self.rect.y + 12)
            elif self.bonus_type == 'damage':
                DamageBonus(self.rect.x + 12, self.rect.y + 12)

            create_particles((self.rect.x, self.rect.y))
            self.kill()
        if pygame.sprite.spritecollideany(self, ships):
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            self.kill()
            pygame.sprite.spritecollideany(self, ships).hp -= 1

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
        if self.hp == 0 or pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.bonus_type == 'life':
                LifeBonus(self.rect.x + 12, self.rect.y + 12)
            elif self.bonus_type == 'damage':
                DamageBonus(self.rect.x + 12, self.rect.y + 12)

            create_particles((self.rect.x, self.rect.y))
            self.kill()
        if pygame.sprite.spritecollideany(self, ships):
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            self.kill()
            pygame.sprite.spritecollideany(self, ships).hp -= 1
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
        if self.hp == 0 or pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.bonus_type == 'life':
                LifeBonus(self.rect.x + 12, self.rect.y + 12)
            elif self.bonus_type == 'damage':
                DamageBonus(self.rect.x + 12, self.rect.y + 12)

            create_particles((self.rect.x, self.rect.y))
            self.kill()
        if pygame.sprite.spritecollideany(self, ships):
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            create_particles((self.rect.x + 25, self.rect.y + 25))
            self.kill()
            pygame.sprite.spritecollideany(self, ships).hp -= 1
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
            self.rect.y -= 4


screen_rect = (0, 0, width, height)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.transform.scale(load_image("boom_particle.png", colorkey=-1), (25, 25))]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.add(particles)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

    def update(self):
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if pygame.sprite.spritecollideany(self, borders):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def gameover(way):
    font_gameover = pygame.font.Font(None, 60)
    font_way = pygame.font.Font(None, 30)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                main_menu()

        gameover_text = font_gameover.render('Игра окончена!', True, pygame.Color('#ffffff'))
        way_text = font_way.render(way, True, pygame.Color('#ffffff'))

        screen.blit(gameover_text, (150, 200))
        screen.blit(way_text, (200, 250))

        pygame.display.flip()


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
            if event.type == pygame.KEYDOWN:
                final_window()

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
    final_window()


def level1():
    Border(5, 5, width - 5, 5)
    baseborder = Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()
    lev_map = load_level('level1.csv')
    cnt = 0
    font = pygame.font.Font(None, 30)

    sprite_appear = pygame.USEREVENT + 1
    pygame.time.set_timer(sprite_appear, 3000)

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
            if event.type == sprite_appear:
                enemy_appear(lev_map[cnt])
                cnt += 1

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            spaceship.update('down')

        if pygame.sprite.spritecollideany(baseborder, enemies):
            spaceship.basehp -= 1
        if spaceship.hp == 0:
            create_particles((spaceship.rect.x + 25, spaceship.rect.y + 25))
            spaceship.kill()
            gameover('Корабль уничтожен!')
        if spaceship.basehp == 0:
            gameover('База уничтожена!')

        player_bullets.update()
        enemies.update()
        bonuses.update()
        particles.update()

        screen.fill(pygame.Color('#000000'))

        text = font.render(f'{spaceship.hp} прочности корабля / {spaceship.basehp} прочности базы', True,
                           pygame.Color('#ffffff'))
        screen.blit(text, (25, height - 60))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)
        enemies.draw(screen)
        bonuses.draw(screen)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(120)


def level2():
    Border(5, 5, width - 5, 5)
    baseborder = Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()
    lev_map = load_level('level2.csv')
    cnt = 0
    font = pygame.font.Font(None, 30)

    sprite_appear = pygame.USEREVENT + 1
    pygame.time.set_timer(sprite_appear, 3000)

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
            if event.type == sprite_appear:
                enemy_appear(lev_map[cnt])
                cnt += 1

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            spaceship.update('down')

        if pygame.sprite.spritecollideany(baseborder, enemies):
            spaceship.basehp -= 1
        if spaceship.hp == 0:
            create_particles((spaceship.rect.x + 25, spaceship.rect.y + 25))
            spaceship.kill()
            gameover('Корабль уничтожен!')
        if spaceship.basehp == 0:
            gameover('База уничтожена!')

        player_bullets.update()
        bonuses.update()
        particles.update()

        screen.fill(pygame.Color('#000000'))

        text = font.render(f'{spaceship.hp} прочности корабля / {spaceship.basehp} прочности базы', True,
                           pygame.Color('#ffffff'))
        screen.blit(text, (25, height - 60))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)
        enemies.draw(screen)
        bonuses.draw(screen)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(120)


def level3():
    Border(5, 5, width - 5, 5)
    baseborder = Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()
    lev_map = load_level('level3.csv')
    cnt = 0
    font = pygame.font.Font(None, 30)

    sprite_appear = pygame.USEREVENT + 1
    pygame.time.set_timer(sprite_appear, 3000)

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
            if event.type == sprite_appear:
                enemy_appear(lev_map[cnt])
                cnt += 1

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            spaceship.update('down')

        if pygame.sprite.spritecollideany(baseborder, enemies):
            spaceship.basehp -= 1
        if spaceship.hp == 0:
            create_particles((spaceship.rect.x + 25, spaceship.rect.y + 25))
            spaceship.kill()
            gameover('Корабль уничтожен!')
        if spaceship.basehp == 0:
            gameover('База уничтожена!')

        player_bullets.update()
        bonuses.update()
        particles.update()

        screen.fill(pygame.Color('#000000'))

        text = font.render(f'{spaceship.hp} прочности корабля / {spaceship.basehp} прочности базы', True,
                           pygame.Color('#ffffff'))
        screen.blit(text, (25, height - 60))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)
        enemies.draw(screen)
        bonuses.draw(screen)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(120)


def level4():
    Border(5, 5, width - 5, 5)
    baseborder = Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()
    lev_map = load_level('level4.csv')
    cnt = 0
    font = pygame.font.Font(None, 30)

    sprite_appear = pygame.USEREVENT + 1
    pygame.time.set_timer(sprite_appear, 3000)

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
            if event.type == sprite_appear:
                enemy_appear(lev_map[cnt])
                cnt += 1

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            spaceship.update('down')

        if pygame.sprite.spritecollideany(baseborder, enemies):
            spaceship.basehp -= 1
        if spaceship.hp == 0:
            create_particles((spaceship.rect.x + 25, spaceship.rect.y + 25))
            spaceship.kill()
            gameover('Корабль уничтожен!')
        if spaceship.basehp == 0:
            gameover('База уничтожена!')

        player_bullets.update()
        bonuses.update()
        particles.update()

        screen.fill(pygame.Color('#000000'))

        text = font.render(f'{spaceship.hp} прочности корабля / {spaceship.basehp} прочности базы', True,
                           pygame.Color('#ffffff'))
        screen.blit(text, (25, height - 60))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)
        enemies.draw(screen)
        bonuses.draw(screen)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(120)


def level5():
    Border(5, 5, width - 5, 5)
    baseborder = Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()
    lev_map = load_level('level5.csv')
    cnt = 0
    font = pygame.font.Font(None, 30)

    sprite_appear = pygame.USEREVENT + 1
    pygame.time.set_timer(sprite_appear, 3000)

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
            if event.type == sprite_appear:
                enemy_appear(lev_map[cnt])
                cnt += 1

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            spaceship.update('down')

        if pygame.sprite.spritecollideany(baseborder, enemies):
            spaceship.basehp -= 1
        if spaceship.hp == 0:
            create_particles((spaceship.rect.x + 25, spaceship.rect.y + 25))
            spaceship.kill()
            gameover('Корабль уничтожен!')
        if spaceship.basehp == 0:
            gameover('База уничтожена!')

        player_bullets.update()
        bonuses.update()
        particles.update()

        screen.fill(pygame.Color('#000000'))

        text = font.render(f'{spaceship.hp} прочности корабля / {spaceship.basehp} прочности базы', True,
                           pygame.Color('#ffffff'))
        screen.blit(text, (25, height - 60))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)
        enemies.draw(screen)
        bonuses.draw(screen)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(120)


def level6():
    Border(5, 5, width - 5, 5)
    baseborder = Border(5, height - 70, width - 5, height - 70)
    Border(5, 5, 5, height - 70)
    Border(width - 5, 5, width - 5, height - 70)

    spaceship = SpaceShip()
    clock = pygame.time.Clock()
    lev_map = load_level('level6.csv')
    cnt = 0
    font = pygame.font.Font(None, 30)

    sprite_appear = pygame.USEREVENT + 1
    pygame.time.set_timer(sprite_appear, 3000)

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
            if event.type == sprite_appear:
                enemy_appear(lev_map[cnt])
                cnt += 1

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            spaceship.update('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            spaceship.update('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            spaceship.update('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            spaceship.update('down')

        if pygame.sprite.spritecollideany(baseborder, enemies):
            spaceship.basehp -= 1
        if spaceship.hp == 0:
            create_particles((spaceship.rect.x + 25, spaceship.rect.y + 25))
            spaceship.kill()
            gameover('Корабль уничтожен!')
        if spaceship.basehp == 0:
            gameover('База уничтожена!')

        player_bullets.update()
        bonuses.update()
        particles.update()

        screen.fill(pygame.Color('#000000'))

        text = font.render(f'{spaceship.hp} прочности корабля / {spaceship.basehp} прочности базы', True,
                           pygame.Color('#ffffff'))
        screen.blit(text, (25, height - 60))

        borders.draw(screen)
        ships.draw(screen)
        player_bullets.draw(screen)
        enemies.draw(screen)
        bonuses.draw(screen)
        particles.draw(screen)

        pygame.display.flip()
        clock.tick(120)


def final_window():
    ask_font = pygame.font.Font(None, 60)
    enter_font = pygame.font.Font(None, 30)

    runnning = True

    while runnning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sys.exit(0)

        screen.fill(pygame.Color('#000000'))

        asktext = ask_font.render('Спасибо за игру!', True, pygame.Color('#ffffff'))
        entertext = enter_font.render('Чтобы выйти, нажмите Enter', True, pygame.Color('#ffffff'))

        screen.blit(asktext, (200, 200))
        screen.blit(entertext, (250, 250))

        pygame.display.flip()


if __name__ == '__main__':
    intro()
    main_menu()
