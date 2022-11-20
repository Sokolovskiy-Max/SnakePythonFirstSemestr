import pygame

import parameters
from parameters import surface

need_input = False
input_text = '|'
tick = 30


def print_text(message, x, y, font_color='white', font_type='font.oTF', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    surface.blit(text, (x, y))


def get_input(x, y):
    global need_input, input_text, tick
    input_rect = pygame.Rect(x, y, 250, 70)

    pygame.draw.rect(parameters.surface, (255, 45, 137), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True

    if need_input:
        for event in pygame.event.get():
            if need_input and event.type == pygame.KEYDOWN:
                input_text = input_text.replace('|', '')
                tick = 30
                if event.key == pygame.K_RETURN:
                    need_input = False
                    message = input_text
                    input_text = ''
                    print_text(message=input_text, x=input_rect.x + 10, y=input_rect.y + 10, font_size=50)
                    return message
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode

                input_text += '|'
    if len(input_text):
        print_text(message=input_text, x=input_rect.x + 10, y=input_rect.y + 10, font_size=50)
    tick -= 1
    if tick == 0:
        input_text = input_text[:-1]
    if tick == -30:
        input_text += '|'
        tick = 30

    return None
