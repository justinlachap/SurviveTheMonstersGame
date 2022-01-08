import sys
import time

from src.player import *
import monster

FPS = 0.05
WIDTH = 742
HEIGHT = 634
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
pygame.init()


background = pygame.display.set_mode((WIDTH, HEIGHT))
player1 = Player(2, 385)
monsters = [monster.Skeleton(100), monster.Goblin(200)]
surf = pygame.image.load(
    os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview', 'Background.png'))
surf = pygame.transform.scale(surf, (surf.get_width() / 1.25, surf.get_height() / 1.25))
last_key = None
background_x = 0

while True:
    if player1.x <= -120:
        player1.x = 610
    elif player1.x >= 610:
        player1.x = -120
    time.sleep(FPS)
    background.fill((0, 0, 0))
    background.blit(surf, (background_x, 0))
    if player1.isGoingRight:
        background.blit(surf, ((background_x - 742), 0))
        background.blit(surf, (WIDTH + background_x, 0))
        if background_x == -WIDTH:
            background.blit(surf, (WIDTH + background_x, 0))
            background_x = 0

    elif not player1.isGoingRight:
        background.blit(surf, (WIDTH + background_x, 0))
        background.blit(surf, ((background_x - WIDTH), 0))
        if background_x == -WIDTH:
            background.blit(surf, (background_x - WIDTH, 0))
            background_x = 0
    player1.draw_health(background)
    background.blit(player1.image, (player1.x, player1.y)
                    )
    for monst in monsters:
        background.blit(monst.image, (monst.x, monst.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            last_key = event.key
    if last_key == pygame.K_RIGHT:
        player1.animate()
        player1.walks(True)
        background_x -= 5
    if last_key == pygame.K_LEFT:
        player1.animate()
        player1.walks(False)
        background_x += 5
    if last_key == pygame.K_DOWN or last_key == None:
        player1.rest()
    if last_key == pygame.K_SPACE:
        if not player1.attacks():
            last_key= None
    if last_key == pygame.K_UP:
        if not player1.jumps():
            last_key = None

    if player1.health == 0:
        player1.dies()
    pygame.display.update()
