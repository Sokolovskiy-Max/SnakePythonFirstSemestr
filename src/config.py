import pygame
from src.Maps import maps
from src.Save import Saves

pygame.init()
RES = 800
SIZE = 50

EAT_SOUND = pygame.mixer.Sound('sounds/Sound_eat.wav')
surface = pygame.display.set_mode([RES, RES])

clock = pygame.time.Clock()
APPLE_IMG = pygame.image.load('images/apple.png')
APPLE_IMG = pygame.transform.scale(APPLE_IMG, (SIZE, SIZE))

MENU_BKCGR = pygame.image.load('images/menu.jpg')
MENU_BKCGR = pygame.transform.scale(MENU_BKCGR, (RES, RES))
FREEZE_IMG = pygame.image.load('images/freeze.png')

BACK1 = pygame.image.load('images/theme1.jpg')
BACK2 = pygame.image.load('images/theme2.jpg')
BACK2 = pygame.transform.scale(BACK2, (RES, RES))
BACK3 = pygame.image.load('images/theme3.jpg')
BACK3 = pygame.transform.scale(BACK3, (RES, RES))

GREEN_ONE = pygame.image.load('images/green_1.png')
GREEN_TWO = pygame.image.load('images/green_2.png')
ROCK_ONE = pygame.image.load('images/rock_1.png')
ROCK_TWO = pygame.image.load('images/rock_2.png')
ROSE_ONE = pygame.image.load('images/rose_1.png')
ROSE_TWO = pygame.image.load('images/rose_2.png')

FREEZE_APPLE = pygame.image.load('images/freeze_apple.png')
FREEZE = pygame.image.load('images/freeze.png')
APPLE = pygame.image.load('images/apple.png')
GOLDEN_APPLE = pygame.image.load('images/golden_apple.png')
ROCK = pygame.image.load('images/rock.png')

INACTIVE_BUTTON_COLOR = (37, 20, 20)
ACTIVE_BUTTON_COLOR = (23, 204, 58)
INPUT_TEXT_COLOR = (255, 45, 137)

back = BACK1
score = 0
level = maps[0]
save_data = Saves()
