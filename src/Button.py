from src.textFunctions import print_text
from src.config import*
pygame.init()


class Button:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = INACTIVE_BUTTON_COLOR
        self.active_color = ACTIVE_BUTTON_COLOR
        self.BUTTON_SOUND = pygame.mixer.Sound('sounds/button.wav')

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            pygame.draw.rect(surface, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(self.BUTTON_SOUND)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
                else:
                    return True

        else:
            pass
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)
