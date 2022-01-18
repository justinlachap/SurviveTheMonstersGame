import sys
import time

import pygame.transform

import monster
from src.player import *

FPS = 0.05
SCREEN_WIDTH, SCREEN_HEIGHT = 742, 634
BUTTON_WIDTH = 100
SCREEN_POS = 30

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_POS, SCREEN_POS)
pygame.init()
background = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player1 = Player(400, 385)
monsters = [monster.Skeleton(50), monster.Goblin(-300)]
surf = pygame.image.load(
    os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview', 'Background.png'))
surf = pygame.transform.scale(surf, (surf.get_width() / 1.25, surf.get_height() / 1.25))
controls = pygame.image.load(
    os.path.join('assets', 'controls.png'))
controls = pygame.transform.scale(controls, (controls.get_width() / 2.5, controls.get_height() / 2.5))

last_key = None
background_x = 0
in_menu = True

pygame.font.init()
font = pygame.font.Font(pygame.font.match_font('arial'), 14)
text1 = 'PLAY'
text2 = 'CONTROLS'
color = (255, 255, 255)
play_button = font.render(text1, True, color)
controls_button = font.render(text2, True, color)
buttons = [pygame.Rect(220, 240, BUTTON_WIDTH, BUTTON_WIDTH / 2), pygame.Rect(370, 240, BUTTON_WIDTH, BUTTON_WIDTH / 2)]


def draw_menu():
    background.blit(surf, (0, 0))
    for i, e in enumerate([(play_button, (253, 255)), (controls_button, ((390, 255)))]):
        pygame.draw.ellipse(surf, [49, 121, 176], buttons[i])
        background.blit(e[0], e[1])


pygame.mixer.init()
pygame.mixer.music.load(os.path.join('assets', 'sounds', 'run.wav'))

music = False
while True:
    if in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if buttons[0].collidepoint(x, y):

                    in_menu = False
                    surf = pygame.image.load(
                        os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview',
                                     'Background.png'))
                    surf = pygame.transform.scale(surf, (surf.get_width() / 1.25, surf.get_height() / 1.25))
                elif buttons[1].collidepoint(x, y):
                    background.blit(controls, (200, 400))
                    pygame.display.update()
                    time.sleep(1.5)

                    in_menu = False
                    surf = pygame.image.load(
                        os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview',
                                     'Background.png'))
                    surf = pygame.transform.scale(surf, (surf.get_width() / 1.25, surf.get_height() / 1.25))
    else:

        time.sleep(FPS)
        rel_x = background_x % surf.get_rect().width
        background.blit(surf, (rel_x - surf.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            background.blit(surf, (rel_x, 0))

        player1.readjust(background)
        background.blit(player1.image, (player1.x, player1.y))
        for monst in monsters:
            background.blit(monst.image, (monst.x, monst.y))
            if monst.has_projectile:
                background.blit(monst.projectile_image, (monst.projectile_x, monst.y + 30))
                print(monst.projectile_x)
                if monst.projectile_x >= player1.x + 85 and monst.x <= player1.x + 95 and player1.jumping_sprite == 0:
                    player1.health -= 20
                    monst.has_projectile = False
                elif monst.projectile_x >= player1.x + 85 and monst.x <= player1.x + 95 and player1.jumping_sprite != 0:
                    monst.has_projectile = False

            monst.update(player1)
            if not monst.has_projectile:
                monst.throw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                last_key = event.key
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(player1.x, monsters[0].x)
        if last_key == pygame.K_RIGHT:
            if not music:
                pygame.mixer.music.play()
                music = True
            player1.animate()
            player1.walks(True)
            background_x -= 5
            for monst in monsters:
                monst.x -= 5
        if last_key == pygame.K_LEFT:
            if not music:
                pygame.mixer.music.play()
                music = True
            player1.animate()
            player1.walks(False)
            background_x += 5
            for monst in monsters:
                monst.x += 5
        if last_key == pygame.K_DOWN or last_key == None:
            if music:
                pygame.mixer.music.stop()
                music = 0
            player1.rest()
        if last_key == pygame.K_SPACE:

            if not player1.attacks():
                pygame.mixer.music.pause()

                sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "sword.mp3"))
                sound.play()
                last_key = None
                new_monsters = monsters
                for enemy in monsters:
                    if player1.isGoingRight and (enemy.x >= player1.x + 71 and enemy.x <= player1.x + 161):
                        new_monsters.remove(enemy)
                    if not player1.isGoingRight and (enemy.x <= player1.x + 44 and player1.x - 90 <= enemy.x):
                        new_monsters.remove(enemy)
                monsters = new_monsters

        if last_key == pygame.K_UP:
            if not player1.jumps():
                last_key = None
                player1.jumping_sprite = 0

        if player1.health == 0:
            player1.dies()
    pygame.display.update()
