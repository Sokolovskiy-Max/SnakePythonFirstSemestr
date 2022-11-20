import pygame

from save import Saves
pygame.init()
RES = 800
SIZE = 50
button_sound = pygame.mixer.Sound('button.wav')
eat_sound = pygame.mixer.Sound('Sound_eat.wav')
surface = pygame.display.set_mode([RES, RES])

clock = pygame.time.Clock()
apple_img1 = pygame.image.load('apple.png')
apple_img = pygame.transform.scale(apple_img1, (SIZE, SIZE))

menu_bkcgr = pygame.image.load('menu.jpg')
menu_bkcgr = pygame.transform.scale(menu_bkcgr, (RES, RES))
freeze_img = pygame.image.load('freeze.png')

back1 = pygame.image.load('theme1.jpg')
back2 = pygame.image.load('theme2.jpg')
back2 = pygame.transform.scale(back2, (RES, RES))
back3 = pygame.image.load('theme3.jpg')
back3 = pygame.transform.scale(back3, (RES, RES))



