import os
import time

import pygame


# image = pygame.image.load(os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'Idle.png'))
# image = pygame.transform.scale(image, (image.get_width()*1.5, image.get_height()*1.5))
def draw_health_bar(surf, pos, size, borderC, backC, healthC, progress):
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos = (pos[0] + 1, pos[1] + 1)
    innerSize = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)


max_health = 100


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.attacking_sprite = 0
        self.x = x
        self.y = y
        self.isGoingRight = True
        self.isAttacking = False
        self.health = 90
        self.running = False
        self.right_srites, self.left_sprites, self.staticR_sprites, self.staticL_sprites, self.attackR_sprites, self.attackL_sprites = [], [], [], [], [], []
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile000.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile001.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile002.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile003.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile004.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile005.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile006.png')))
        self.right_srites.append(pygame.image.load(
            os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                         'tile007.png')))
        for i in range(0, 8):
            self.attackR_sprites.append(pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites',
                             'attacker',
                             'tile00{}.png'.format(i))))
        for i, e in enumerate(self.attackR_sprites):
            newIm = pygame.transform.scale(e, (e.get_height() * 1.5, e.get_width() * 1.5))
            self.attackR_sprites[i] = newIm
        for i in range(0, 10):
            self.staticR_sprites.append(pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'static',
                             'tile00{}.png'.format(i))))
        for i, e in enumerate(self.right_srites):
            newIm = pygame.transform.scale(e, (e.get_height() * 1.5, e.get_width() * 1.5))
            self.right_srites[i] = newIm

        for i, e in enumerate(self.staticR_sprites):
            newIm = pygame.transform.scale(e, (e.get_height() * 1.5, e.get_width() * 1.5))
            self.staticR_sprites[i] = newIm

        for sprite in self.right_srites:
            self.left_sprites.append(pygame.transform.flip(sprite, True, False))
        for sprite in self.staticR_sprites:
            self.staticL_sprites.append(pygame.transform.flip(sprite, True, False))
        for sprite in self.attackR_sprites:
            self.attackL_sprites.append(pygame.transform.flip(sprite,True,False))

        self.current_sprite = 0
        self.image = self.staticR_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def animate(self):
        self.running = True

    def rest(self):
        if self.isGoingRight:
            self.current_sprite += 1
            if self.current_sprite >= len(self.staticR_sprites) or self.current_sprite < 0:
                self.current_sprite = 0
            self.image = self.staticR_sprites[self.current_sprite]
        else:
            self.current_sprite -= 1
            if -self.current_sprite >= len(self.staticL_sprites) or self.current_sprite > 0:
                self.current_sprite = 0
            self.image = self.staticL_sprites[self.current_sprite]

    def walks(self, right):
        if right and self.running:
            self.x += 4
            self.current_sprite += 1
            if self.current_sprite >= len(self.right_srites) or self.current_sprite < 0:
                self.current_sprite = 0

            self.image = self.right_srites[self.current_sprite]
            self.isGoingRight = True

        elif not right and self.running:
            self.x -= 4
            self.current_sprite -= 1
            if self.current_sprite > 0 or -self.current_sprite >= len(self.left_sprites):
                self.current_sprite = 0

            self.image = self.left_sprites[-self.current_sprite]
            self.isGoingRight = False

    def draw_health(self, surf):
        health_rect = pygame.Rect(self.x + 107, self.y + 68, self.image.get_width() / 9, 10)

        draw_health_bar(surf, health_rect.topleft, health_rect.size,
                        (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health / max_health)

    def attacks(self):
        if self.isGoingRight:
            self.image = self.attackR_sprites[self.attacking_sprite]
            self.attacking_sprite += 1

            if self.attacking_sprite >= len(self.attackR_sprites) or self.attacking_sprite < 0:
                self.attacking_sprite = 0
                return False

        else:
            self.image = self.attackL_sprites[self.attacking_sprite]
            self.attacking_sprite += 1

            if self.attacking_sprite >= len(self.attackL_sprites) or self.attacking_sprite < 0:
                self.attacking_sprite = 0
                return False
        return True




