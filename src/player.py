import os

import pygame


# source: https://stackoverflow.com/questions/64867475/how-to-put-a-health-bar-over-the-sprite-in-pygame
def draw_health_bar(surf, pos, size, borderC, backC, healthC, progress):
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos = (pos[0] + 1, pos[1] + 1)
    innerSize = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)


MAX_HEALTH = 100
SCALE = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.attacking_sprite, self.jumping_sprite = 0, 0
        self.x = x
        self.y = y
        self.isGoingRight = True
        self.isAttacking = False
        self.health = 100
        self.running = False

        self.right_sprites, self.left_sprites, self.staticR_sprites, self.staticL_sprites, self.attackR_sprites, self.attackL_sprites, self.jumpR_sprites, self.jumpL_sprites = [], [], [], [], [], [], [], []
        self.generateSprites()

        self.current_sprite = 0
        self.image = self.staticR_sprites[self.current_sprite]
        self.wait = 0

    def animate(self):
        self.running = True

    def rest(self):
        self.y = 385
        if self.wait % 2 == 0:
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
        self.wait += 1

    def walks(self, right):
        self.y = 385
        if right and self.running:
            self.x += 4
            self.current_sprite += 1
            if self.current_sprite >= len(self.right_sprites) or self.current_sprite < 0:
                self.current_sprite = 0

            self.image = self.right_sprites[self.current_sprite]
            self.isGoingRight = True

        elif not right and self.running:
            self.x -= 4
            self.current_sprite -= 1
            if self.current_sprite > 0 or -self.current_sprite >= len(self.left_sprites):
                self.current_sprite = 0

            self.image = self.left_sprites[-self.current_sprite]
            self.isGoingRight = False

    def draw_health(self, surf):
        health_rect = pygame.Rect(self.x + 145, self.y + 88, self.image.get_width() / 9, 10)
        draw_health_bar(surf, health_rect.topleft, health_rect.size,
                        (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health / MAX_HEALTH)

    def attacks(self):
        self.y = 385
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

    def jumps(self):
        if self.jumping_sprite <= 2:
            self.y -= 20
        else:
            self.y += 20


        if self.isGoingRight:
            self.image = self.jumpR_sprites[self.jumping_sprite]
            self.jumping_sprite += 1

            if self.jumping_sprite >= len(self.jumpR_sprites) or self.jumping_sprite < 0:
                self.jumping_sprite = 0
                return False

        else:
            self.image = self.jumpL_sprites[self.jumping_sprite]
            self.jumping_sprite += 1

            if self.jumping_sprite >= len(self.jumpL_sprites) or self.jumping_sprite < 0:
                self.jumping_sprite = 0
                return False
        return True

    def dies(self):
        pass

    def generateSprites(self):
        num_walking_sprites = 8
        num_jumping_sprites = 6
        num_static_sprites = 10

        for i in range(num_walking_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                             'tile00{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.right_sprites.append(newIm)
            self.left_sprites.append(pygame.transform.flip(newIm, True, False))

        for i in range(num_jumping_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'jump',
                             'tile00{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.jumpR_sprites.append(newIm)
            self.jumpL_sprites.append(pygame.transform.flip(newIm, True, False))

        for i in range(num_walking_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites',
                             'attacker',
                             'tile00{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.attackR_sprites.append(newIm)
            self.attackL_sprites.append(pygame.transform.flip(newIm, True, False))

        for i in range(num_static_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'static',
                             'tile00{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.staticR_sprites.append(newIm)
            self.staticL_sprites.append(pygame.transform.flip(newIm, True, False))

    def readjust(self, bg):
        self.draw_health(bg)
        if self.x <= -120:
            self.x = 610
        elif self.x >= 610:
            self.x = -120
