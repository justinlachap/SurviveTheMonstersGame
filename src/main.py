from random import choice
from sys import exit
from time import sleep
import monster
from src.player import *
from src.static.csts import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_POS, SCREEN_POS)
pygame.init()
background = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player_1 = None
monsters = None
last_key = None
surface = pygame.image.load(
    os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview', 'Background.png'))
surface = pygame.transform.scale(surface, (surface.get_width() / 1.25, surface.get_height() / 1.25))
controls = pygame.image.load(
    os.path.join('assets', 'controls.png'))
controls = pygame.transform.scale(controls, (controls.get_width() / 2.5, controls.get_height() / 2.5))
background_x = 0
in_menu = True
pygame.font.init()
font = pygame.font.Font(pygame.font.match_font(DEFAULT_FONT_FAMILY), DEFAULT_FONT_SIZE)
text1, text2 = 'PLAY', 'CONTROLS'
color = COLOR_WHITE
play_button = font.render(text1, True, color)
controls_button = font.render(text2, True, color)
buttons = [pygame.Rect(220, 240, BUTTON_WIDTH, BUTTON_WIDTH / 2), pygame.Rect(370, 240, BUTTON_WIDTH, BUTTON_WIDTH / 2)]


def draw_menu():
    background.blit(surface, (0, 0))
    for j, e in enumerate([(play_button, (253, 255)), (controls_button, (390, 255))]):
        pygame.draw.ellipse(surface, COLOR_BTN_CTRL, buttons[j])
        background.blit(e[0], e[1])


# On devrait faire une classe pour garder les monsters au lieu de passer par réf.
def filter_monsters(_monsters, player):
    # Idéalement on utiliserait filter/lambda pour le bloc de code suivant
    new_monsters = _monsters
    for enemy in _monsters:
        if player.is_going_right and player.x + 161 > enemy.x >= player.x + 71 or (
                not player.is_going_right and player.x - 90 < enemy.x <= player.x + 44):
            new_monsters.remove(enemy)
    return new_monsters


def generate_new_monsters(_monsters, player):
    return _monsters + [choice([monster.Skeleton(player.x - 500), monster.Goblin(player.x - 500)])] if (
                len(_monsters) < 2) else _monsters


pygame.mixer.init()
pygame.mixer.music.load(os.path.join('assets', 'sounds', 'run.wav'))
music = False
while True:
    pygame.display.update()
    if in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if not event.type == pygame.MOUSEBUTTONDOWN:
                continue
            x, y = event.pos
            if not (buttons[0].collidepoint(x, y) or buttons[1].collidepoint(x, y)):
                continue
            in_menu = False
            player_1 = Player(400, 385)
            monsters = [monster.Skeleton(50), monster.Goblin(-300)]
            last_key = None
            surface = pygame.image.load(
                os.path.join('assets', 'Free Pixel Art Forest', 'Free Pixel Art Forest', 'Preview',
                             'Background.png'))
            surface = pygame.transform.scale(surface, (surface.get_width() / 1.25, surface.get_height() / 1.25))
            if not buttons[1].collidepoint(x, y):
                continue
            background.blit(controls, (200, 400))
            pygame.display.update()
            sleep(1.5)
        continue
    sleep(FPS)
    rel_x = background_x % surface.get_rect().width
    background.blit(surface, (rel_x - surface.get_rect().width, 0))
    if rel_x < SCREEN_WIDTH:
        background.blit(surface, (rel_x, 0))
    player_1.readjust(background)
    background.blit(player_1.image, (player_1.x, player_1.y))
    for monst in monsters:
        background.blit(monst.image, (monst.x, monst.y))
        if not monst.has_projectile:
            monst.update(player_1)
            monst.throw()
            continue
        background.blit(monst.projectile_image, (monst.projectile_x, monst.y + 30))
        if not (monst.projectile_x >= player_1.x + 85 and monst.x <= player_1.x + 95):
            monst.update(player_1)
            continue
        monst.has_projectile = False
        if player_1.jumping_sprite == 0:
            player_1.health -= 15
        monst.update(player_1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            last_key = event.key
    if last_key == pygame.K_RIGHT or last_key == pygame.K_d:
        if not music:
            pygame.mixer.music.play()
            music = True
        player_1.animate()
        player_1.walks(True)
        background_x -= 5
        for monst in monsters:
            monst.x -= 5
    if last_key == pygame.K_LEFT or last_key == pygame.K_a:
        if not music:
            pygame.mixer.music.play()
            music = True
        player_1.animate()
        player_1.walks(False)
        background_x += 5
        for monst in monsters:
            monst.x += 5
    if last_key == pygame.K_DOWN or last_key == pygame.K_s or not last_key:
        if music:
            pygame.mixer.music.stop()
            music = False
        if player_1.health > 0:
            player_1.rest()
    if last_key == pygame.K_SPACE and not player_1.attacks():
        pygame.mixer.music.pause()
        sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "sword.mp3"))
        sound.play()
        last_key = None
        monsters = filter_monsters(monsters, player_1)
        monsters = generate_new_monsters(monsters, player_1)
    if (last_key == pygame.K_UP or last_key == pygame.K_w) and not player_1.jumps():
        last_key = None
        player_1.jumping_sprite = 0
    if player_1.health <= 0:
        if music:
            pygame.mixer.music.stop()
            music = False
        for i in range(7):
            sleep(0.2)
            player_1.dies()
            background.blit(surface, (rel_x - surface.get_rect().width, 0))
            background.blit(player_1.image, (player_1.x, player_1.y))
            pygame.display.update()
        in_menu = True
