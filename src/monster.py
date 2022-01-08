import pygame
import os

MAX_HEALTH = 100
SCALE = 1.5

class Monster:
    def __init__(self,x):
        self.x = x
        self.health = 100
        self.right_sprites = []
        self.left_sprites = []
        self.current_sprite = 0






class Goblin(Monster):
    def __init__(self, x):
        super().__init__(x)
        self.generateSprites()
        self.image = self.right_sprites[self.current_sprite]
        self.y = 430
    def generateSprites(self):
        num_attack_sprites = 12
        for i in range(num_attack_sprites):
            if i <= 9:
                oldIm = pygame.image.load(
                    os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Monster_Creatures_Fantasy(Version 1.3)', 'Goblin', 'attack',
                                 'tile00{}.png'.format(i)))
            else:
                oldIm = pygame.image.load(
                    os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)',
                                 'Monster_Creatures_Fantasy(Version 1.3)', 'Goblin', 'attack',
                                 'tile0{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.right_sprites.append(newIm)
            self.left_sprites.append(pygame.transform.flip(newIm, True, False))

class Skeleton(Monster):
    def __init__(self, x):
        super().__init__(x)
        self.generateSprites()
        self.image = self.right_sprites[self.current_sprite]
        self.y = 433
    def generateSprites(self):
        num_attack_sprites = 6
        for i in range(num_attack_sprites):
            oldIm = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)',
                             'Monster_Creatures_Fantasy(Version 1.3)', 'Skeleton', 'attack',
                             'tile00{}.png'.format(i)))
            newIm = pygame.transform.scale(oldIm, (oldIm.get_height() * SCALE, oldIm.get_width() * SCALE))
            self.right_sprites.append(newIm)
            self.left_sprites.append(pygame.transform.flip(newIm, True, False))
