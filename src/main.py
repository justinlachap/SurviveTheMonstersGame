import sys

from src.player import *

FPS = 0.05
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
pygame.init()

background = pygame.display.set_mode((742, 634))
player1 = Player(2, 435)
surf = pygame.image.load(
    os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview', 'Background.png'))
surf = pygame.transform.scale(surf, (surf.get_width() / 1.25, surf.get_height() / 1.25))
print(surf.get_width(), surf.get_height())
last_key = None
background_x = 0

while True:
    time.sleep(FPS)
    background.fill((0, 0, 0))
    background.blit(surf, (background_x, 0))
    if player1.isGoingRight:
        background.blit(surf, ((background_x - surf.get_width()), 0))
        background.blit(surf, (surf.get_width() + background_x, 0))
        if background_x == -surf.get_width():
            background.blit(surf, (surf.get_width() + background_x, 0))
            background_x = 0
    elif not player1.isGoingRight:
        background.blit(surf, (surf.get_width() + background_x, 0))
        background.blit(surf, ((background_x - surf.get_width()), 0))
        if background_x == -surf.get_width():
            background.blit(surf, (background_x - surf.get_width(), 0))
            background_x = 0
    player1.draw_health(background)
    background.blit(player1.image, (player1.x, player1.y)
                    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            last_key = event.key
    if last_key == pygame.K_RIGHT:
        player1.animate()
        player1.walks(True)
        background_x -= 8
    if last_key == pygame.K_LEFT:
        player1.animate()
        player1.walks(False)
        background_x += 8
    if last_key == pygame.K_DOWN or last_key == None:
        player1.rest()
    if last_key == pygame.K_SPACE:
        if not player1.attacks():
            last_key= None

    pygame.display.update()
