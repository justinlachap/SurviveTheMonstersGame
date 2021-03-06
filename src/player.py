import os
import pygame
from src.static.csts import *


# source: https://stackoverflow.com/questions/64867475/how-to-put-a-health-bar-over-the-sprite-in-pygame
def draw_health_bar(surf, pos, size, border_c, back_c, health_c, progress):
    pygame.draw.rect(surf, back_c, (*pos, *size))
    pygame.draw.rect(surf, border_c, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    pygame.draw.rect(surf, health_c,
                     (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1])))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.attacking_sprite, self.jumping_sprite, self.death_sprite = 0, 0, 0
        self.right_sprites, self.left_sprites, self.staticR_sprites, self.staticL_sprites, self.attackR_sprites, self.attackL_sprites, self.jumpR_sprites, self.jumpL_sprites, self.deathR_sprites, self.right_sprites, self.left_sprites, self.staticR_sprites, self.staticL_sprites, self.attackR_sprites, self.attackL_sprites, self.jumpR_sprites, self.jumpL_sprites, self.deathL_sprites = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        self.x = x
        self.y = y
        self.is_going_right = True
        self.is_attacking = False
        self.health = 100
        self.running = False
        self.generate_sprites()
        self.current_sprite = 0
        self.image = self.staticR_sprites[self.current_sprite]
        self.wait = 0

    def animate(self):
        self.running = True

    def rest(self):
        self.y = 385
        if not self.wait % 2 == 0:
            self.wait += 1
            return None
        self.change_sprite()
        if self.is_going_right:
            if self.current_sprite >= len(self.staticR_sprites) or self.current_sprite < 0:
                self.current_sprite = 0
            self.image = self.staticR_sprites[self.current_sprite]
        else:
            if -self.current_sprite >= len(self.staticL_sprites) or self.current_sprite > 0:
                self.current_sprite = 0
            self.image = self.staticL_sprites[self.current_sprite]
        self.wait += 1

    def change_sprite(self):
        self.current_sprite = self.current_sprite + 1 if self.is_going_right else self.current_sprite - 1

    def walks(self, right):
        self.y = 385
        if right and self.running:
            self.x += 4
            self.current_sprite += 1
            if self.current_sprite >= len(self.right_sprites) or self.current_sprite < 0:
                self.current_sprite = 0
            self.image = self.right_sprites[self.current_sprite]
            self.is_going_right = True
        elif not right and self.running:
            self.x -= 4
            self.current_sprite -= 1
            if self.current_sprite > 0 or -self.current_sprite >= len(self.left_sprites):
                self.current_sprite = 0
            self.image = self.left_sprites[-self.current_sprite]
            self.is_going_right = False

    def draw_health(self, surf):
        health_rect = pygame.Rect(self.x + 145, self.y + 88, self.image.get_width() / 9, 10)
        draw_health_bar(surf, health_rect.topleft, health_rect.size,
                        (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health / PLAYER_MAX_HEALTH)

    def attacks(self):
        self.y = 385
        if self.is_going_right:
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
        self.y = self.y - 20 if self.jumping_sprite <= 2 else self.y + 20
        self.jumping_sprite += 1
        self.image = self.jumpR_sprites[self.jumping_sprite - 1] if self.is_going_right else self.jumpL_sprites[
            self.jumping_sprite - 1]
        if self.jumping_sprite >= len(self.jumpL_sprites) or self.jumping_sprite < 0:
            self.jumping_sprite = 0
            return False
        return True

    def dies(self):
        if self.is_going_right:
            self.image = self.deathR_sprites[self.death_sprite]
            self.death_sprite += 1
        else:
            self.image = self.deathL_sprites[self.death_sprite]
            self.death_sprite += 1

    def generate_sprites(self):
        num_walking_sprites = 8
        num_jumping_sprites = 6
        num_static_sprites = 10
        num_death_sprites = 7
        for i in range(num_walking_sprites):
            old_image = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'run',
                             'tile00{}.png'.format(i)))
            new_image = pygame.transform.scale(old_image, (old_image.get_height() * PLAYER_SCALE, old_image.get_width() * PLAYER_SCALE))
            self.right_sprites.append(new_image)
            self.left_sprites.append(pygame.transform.flip(new_image, True, False))
        for i in range(num_jumping_sprites):
            old_image = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'jump',
                             'tile00{}.png'.format(i)))
            new_image = pygame.transform.scale(old_image, (old_image.get_height() * PLAYER_SCALE, old_image.get_width() * PLAYER_SCALE))
            self.jumpR_sprites.append(new_image)
            self.jumpL_sprites.append(pygame.transform.flip(new_image, True, False))
        for i in range(num_walking_sprites):
            old_image = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites',
                             'attacker',
                             'tile00{}.png'.format(i)))
            new_image = pygame.transform.scale(old_image, (old_image.get_height() * PLAYER_SCALE, old_image.get_width() * PLAYER_SCALE))
            self.attackR_sprites.append(new_image)
            self.attackL_sprites.append(pygame.transform.flip(new_image, True, False))
        for i in range(num_static_sprites):
            old_image = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'static',
                             'tile00{}.png'.format(i)))
            new_image = pygame.transform.scale(old_image, (old_image.get_height() * PLAYER_SCALE, old_image.get_width() * PLAYER_SCALE))
            self.staticR_sprites.append(new_image)
            self.staticL_sprites.append(pygame.transform.flip(new_image, True, False))
        for i in range(num_death_sprites):
            old_image = pygame.image.load(
                os.path.join('assets', 'Monster_Creatures_Fantasy(Version 1.3)', 'Fantasy Warrior', 'Sprites', 'death',
                             'tile00{}.png'.format(i)))
            new_image = pygame.transform.scale(old_image, (old_image.get_height() * PLAYER_SCALE, old_image.get_width() * PLAYER_SCALE))
            self.deathR_sprites.append(new_image)
            self.deathL_sprites.append(pygame.transform.flip(new_image, True, False))

    def readjust(self, bg):
        self.draw_health(bg)
        if self.x <= -120:
            self.x = 610
        elif self.x >= 610:
            self.x = -120
