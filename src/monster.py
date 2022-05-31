import os

import pygame

MAX_HEALTH = 100
SCALE = 1.5


class Monster:
    def __init__(self, x):
        self.x = x
        self.health = 100
        self.right_sprites = []
        self.left_sprites = []
        self.current_sprite = 0
        self.isGoingRight = True
        self.wait = 0
        self.count = 0
        self.starts_attacking = 100
        self.has_projectile = False
        self.projectile_x = None
        self.projectile_isGoingRight = None

        self.current_throw_sprite = 0
        self.proj_sprites = []
        self.image, self.projectile_image = None, None

    def update(self, player):

        self.isGoingRight = False if player.x < self.x else True

        if self.isGoingRight:
            if self.current_sprite >= len(self.right_sprites):
                self.current_sprite = 0
            self.image = self.right_sprites[self.current_sprite]
        else:
            if self.current_sprite >= len(self.left_sprites):
                self.current_sprite = 0
            self.image = self.left_sprites[self.current_sprite]

        if not self.has_projectile:
            return None

        self.projectile_image = self.proj_sprites[self.current_throw_sprite]
        self.current_sprite = 0
        if self.projectile_isGoingRight:
            if self.projectile_x - 120 > player.x:
                self.has_projectile = False
                self.projectile_isGoingRight = None
            else:
                if player.image in player.left_sprites:
                    self.projectile_x += 12
                elif player.image in player.right_sprites:
                    self.projectile_x += 4
                else:
                    self.projectile_x += 8
        elif not self.projectile_isGoingRight:
            if self.projectile_x - 40 < player.x:
                self.has_projectile = False
                self.projectile_isGoingRight = None
            else:
                if player.image in player.left_sprites:
                    self.projectile_x -= 4
                elif player.image in player.right_sprites:
                    self.projectile_x -= 12
                else:
                    self.projectile_x -= 8

    def throw(self):
        if self.current_sprite == abs(len(self.left_sprites)) - 1:
            self.has_projectile = True
            self.projectile_isGoingRight = self.isGoingRight
            self.projectile_x = self.x + 65 if self.isGoingRight else self.x - 5
        else:
            self.current_sprite += 1


class Goblin(Monster):
    def __init__(self, x):
        super().__init__(x)
        self.generateSprites()
        self.image = self.right_sprites[self.current_sprite]
        self.y = 430
        self.count, starts_attacking = 0, 100

        self.projectile_image = self.proj_sprites[self.current_throw_sprite]

    def generateSprites(self):
        num_attack_sprites, num_throw_sprites = 12, 19
        for i in range(num_attack_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)',
                             'Monster_Creatures_Fantasy(Version 1.3)', 'Goblin', 'attack',
                             ('tile00{}.png' if i <= 9 else 'tile0{}.png').format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.right_sprites.append(newIm)
            self.left_sprites.append(pygame.transform.flip(newIm, True, False))

        for i in range(num_throw_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)',
                             'Monster_Creatures_Fantasy(Version 1.3)', 'Goblin', 'projectile',
                             ('tile00{}.png' if i <= 9 else 'tile0{}.png').format(i)))
            self.proj_sprites.append(
                pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE)))


class Skeleton(Monster):
    def __init__(self, x):
        super().__init__(x)
        self.generateSprites()
        self.image = self.right_sprites[self.current_sprite]
        self.y = 433
        self.projectile_image = self.proj_sprites[self.current_throw_sprite]

    def generateSprites(self):
        num_attack_sprites, num_throw_sprites = 6, 8
        for i in range(num_attack_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)',
                             'Monster_Creatures_Fantasy(Version 1.3)', 'Skeleton', 'attack',
                             'tile00{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.right_sprites.append(newIm)
            self.left_sprites.append(pygame.transform.flip(newIm, True, False))
        for i in range(num_throw_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)',
                             'Monster_Creatures_Fantasy(Version 1.3)', 'Skeleton', 'projectile',
                             'tile00{}.png'.format(i)))
            self.proj_sprites.append(
                pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE)))
