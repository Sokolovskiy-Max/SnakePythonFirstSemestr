from random import randrange
from src.config import *
from src.Button import Button
from src.highscore import *
from src.Maps import maps
from src.highscore import high_scores


def game_engine():

    game_app = GameApp()
    while game_app.game:
        game_app.draw_elements()
        game_app.change_direction()
        game_app.draw_snake()
        clock.tick(
            game_app.fps * (1 + game_app.grass.count_on_grass(game_app.snake) / game_app.length) *
            (1 - 0.5 * game_app.sand.count_on_sand(game_app.snake) / game_app.length))
        surface.blit(back, (0, 0))
        game_app.k += 1

        game_app.tait_direction()
        # game_app.check_bonus()
        game_app.check_eatings()
    return game_over()


class GameApp:
    def __init__(self):
        self.game = True

        self.grass = Grass(level)
        self.sand = Sand(level)
        self.rocks = Rocks(level)

        self.apple = Apple(self.rocks)
        self.fr_apple = FreezeApple(self.rocks)
        self.golden_apple = GoldenApple(self.rocks)
        self.length = 1
        self.x, self.y = find_spawn(level)
        self.snake = [(self.x, self.y)]
        self.dx, self.dy = 0, 0
        self.tail_dx, self.tail_dy = 0, 0
        self.fps = 180
        self.dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
        self.score = 0
        self.speed_count, self.snake_speed = 0, 1
        self.font_score = pygame.font.SysFont('font.oTF', 50, bold=True)
        self.tdx = 0
        self.tdy = 0
        self.freeze = Freeze(self.rocks)
        self.freeze_exist = 0
        self.freeze_apple_exist = 0
        self.golden_apple_exist = 0
        self.k = 0

    def draw_elements(self):
        surface.blit(back, (0, 0))
        self.grass.draw()
        self.sand.draw()
        self.rocks.draw()
        if (self.dx, self.dy) == (0, 0):
            [pygame.draw.rect(surface, pygame.Color('orange'), (i, j, SIZE - 1, SIZE - 1)) for i, j in self.snake]
        if self.freeze_exist:
            surface.blit(FREEZE_IMG, (self.freeze.x, self.freeze.y, SIZE, SIZE))

        # apple.draw()
        surface.blit(APPLE_IMG, (self.apple.x, self.apple.y, SIZE, SIZE))
        if self.freeze_apple_exist:
            self.fr_apple.draw()
        if self.golden_apple_exist:
            self.golden_apple.draw()
        # show score
        render_score = self.font_score.render(f'SCORE: {self.score}', True, pygame.Color('orange'))
        surface.blit(render_score, (5, 5))

    def change_direction(self):
        key = pygame.key.get_pressed()
        if self.dx == self.tdx and self.dy == self.tdy:
            if key[pygame.K_w]:
                if self.dirs['W']:
                    self.tdx, self.tdy = 0, -1
                    self.dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
            elif key[pygame.K_s]:
                if self.dirs['S']:
                    self.tdx, self.tdy = 0, 1
                    self.dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
            elif key[pygame.K_a]:
                if self.dirs['A']:
                    self.tdx, self.tdy = -1, 0
                    self.dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
            elif key[pygame.K_d]:
                if self.dirs['D']:
                    self.tdx, self.tdy = 1, 0
                    self.dirs = {'W': True, 'S': True, 'A': False, 'D': True, }

    def draw_snake(self):
        if self.dx == 1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[-1][0] - 1, self.snake[-1][1], self.k, SIZE - 1))
        if self.dx == -1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[-1][0] + SIZE - self.k, self.snake[-1][1], self.k, SIZE - 1))
        if self.dy == 1:
            pygame.draw.rect(surface, pygame.Color('orange'), (self.snake[-1][0], self.snake[-1][1], SIZE - 1, self.k))
        if self.dy == -1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[-1][0], self.snake[-1][1] + SIZE - self.k, SIZE - 1, self.k))
        if self.tail_dx == 1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[0][0] + self.k - SIZE, self.snake[0][1], SIZE - 1 - self.k, SIZE - 1))
        if self.tail_dy == 1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[0][0], self.snake[0][1] + self.k - SIZE, SIZE - 1, SIZE - self.k))
        if self.tail_dx == -1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[0][0] + SIZE, self.snake[0][1], SIZE - self.k, SIZE - 1))
        if self.tail_dy == -1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (self.snake[0][0], self.snake[0][1] + SIZE, SIZE - 1, SIZE - self.k))

        [pygame.draw.rect(surface, pygame.Color('orange'), (i, j, SIZE - 1, SIZE - 1)) for i, j in self.snake[:-1]]
        pygame.display.flip()

    def tait_direction(self):
        if self.k == SIZE:
            self.dx, self.dy = self.tdx, self.tdy
            if len(self.snake) > 1:
                if self.snake[0][0] > self.snake[1][0]:
                    self.tail_dx = -1
                    self.tail_dy = 0
                elif self.snake[0][0] < self.snake[1][0]:
                    self.tail_dx = 1
                    self.tail_dy = 0
                elif self.snake[0][1] > self.snake[1][1]:
                    self.tail_dy = -1
                    self.tail_dx = 0
                elif self.snake[0][1] < self.snake[1][1]:
                    self.tail_dy = 1
                    self.tail_dx = 0
            else:
                self.tail_dx, self.tail_dy = self.dx, self.dy
            render_score = self.font_score.render(f'SCORE: {self.score}', True, pygame.Color('orange'))
            surface.blit(render_score, (5, 5))
            self.check_bonus()

    def check_bonus(self):
        if self.freeze_exist == 0:
            if 1 // randrange(1, 250):
                self.freeze = Freeze(self.rocks)
                self.freeze_exist = 1
        if self.freeze_apple_exist == 0:
            if 1 // randrange(1, 250):
                self.fr_apple = FreezeApple(self.rocks)
                self.freeze_apple_exist = 1
        if self.golden_apple_exist == 0:
            if 1 // randrange(1, 500):
                self.golden_apple = GoldenApple(self.rocks)
                self.golden_apple_exist = 1
        self.x += self.dx * SIZE
        self.y += self.dy * SIZE
        self.snake.append((self.x, self.y))
        self.snake = self.snake[-self.length:]
        self.speed_count += 1
        self.k = 0

    def check_eatings(self):
        if self.snake[-1] == (self.apple.x, self.apple.y):
            pygame.mixer.Sound.play(EAT_SOUND)
            self.apple = Apple(self.rocks)
            surface.blit(APPLE_IMG, (self.apple.x, self.apple.y, SIZE, SIZE))
            self.length += 1
            self.score += 1
            self.fps += 20
        if self.freeze_apple_exist == 1 and self.snake[-1] == (self.fr_apple.x, self.fr_apple.y):
            pygame.mixer.Sound.play(EAT_SOUND)
            self.score += 1
            self.length += 4
            self.fps -= self.fr_apple.power
            self.freeze_apple_exist = 0
        if self.freeze_exist == 1 and self.snake[-1] == (self.freeze.x, self.freeze.y):
            pygame.mixer.Sound.play(EAT_SOUND)
            self.score -= 2
            self.fps -= self.freeze.power
            self.freeze_exist = 0
        if self.golden_apple_exist == 1 and self.snake[-1] == (self.golden_apple.x, self.golden_apple.y):
            pygame.mixer.Sound.play(EAT_SOUND)
            self.score += 5
            self.length += 5
            self.golden_apple_exist = 0
        if self.x < 0 or self.x > RES - SIZE or self.y < 0 or self.y > RES - SIZE or len(self.snake) != len(set(self.snake)):
            self.game = False
        if any((i[0] * SIZE, i[1] * SIZE) == self.snake[-1] for i in self.rocks.pos):
            self.game = False
        close_game()


def game_over():
    stopped = True
    got_name = False
    while stopped:
        close_game()
        surface.blit(back, (0, 0))
        print_text('Game over. Press Tab to play again, Esc to exit.', 40, 50)
        if not got_name:
            print_text('Enter your name: ', 40, 150)
            name = get_input(40, 200)
            if name:
                got_name = True
                high_scores.update(name, score)
        else:
            print_text('Name', 40, 150)
            print_text('Scores', 290, 150)
            high_scores.print(40, 200)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            return True
        if keys[pygame.K_ESCAPE]:
            save_data.add('max', score)
            save_data.add('hs', high_scores.hs_table)
            return False

        pygame.display.update()


def find_spawn(level):
    for i in range(RES // SIZE):
        for j in range(RES // SIZE):
            if level[i][j] == 5:
                return j * SIZE, i * SIZE


def start_game():
    choose_theme()
    while game_engine():
        pass


def show_menu():
    start_btn = Button(254, 70)
    level_btn = Button(120, 70)
    quit_btn = Button(108, 70)

    start_btn.draw(148, 270, 'Start game', start_game, 50)
    level_btn.draw(328, 400, 'Level', level_menu, 50)
    quit_btn.draw(508, 530, 'Quit', quit, 50)

    show = True

    while show:
        close_game()

        surface.blit(MENU_BKCGR, (0, 0))

        start_btn.draw(280, 270, 'Start game', start_game, 50)
        level_btn.draw(328, 400, 'Level', level_menu, 50)
        quit_btn.draw(336, 530, 'Quit', quit, 50)

        # get_input(50,200)
        pygame.display.update()
        clock.tick(60)


class Rectangle(object):
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self):
        pygame.draw.rect(surface, pygame.Color(self.color), (self.x, self.y, SIZE, SIZE))


class Rocks:
    def __init__(self, all_pos):
        pos = []
        for i in range(RES // SIZE):
            for j in range(RES // SIZE):
                if all_pos[i][j] == 1:
                    pos.append([j, i])
        self.pos = pos
        self.rock_png = ROCK.convert_alpha()
        self.rock_1 = ROCK_ONE.convert_alpha()
        self.rock_2 = ROCK_TWO.convert_alpha()

    def draw(self):
        for i in self.pos:
            if (i[0] % 2 == 0 and i[1] % 2 == 0) or (i[0] % 2 == 1 and i[1] % 2 == 1):
                surface.blit(self.rock_1, (i[0] * SIZE, i[1] * SIZE))
            else:
                surface.blit(self.rock_2, (i[0] * SIZE, i[1] * SIZE))
        for i in self.pos:
            surface.blit(self.rock_png, (i[0] * SIZE, i[1] * SIZE))

    def in_rock(self, x, y):
        return [x, y] in self.pos


class Grass:
    def __init__(self, all_pos):
        pos = []
        for i in range(RES // SIZE):
            for j in range(RES // SIZE):
                if all_pos[i][j] == 2:
                    pos.append([j, i])
        self.pos = pos
        self.green_1 = GREEN_ONE.convert_alpha()
        self.green_2 = GREEN_TWO.convert_alpha()

    def draw(self):
        for i in self.pos:
            if (i[0] % 2 == 0 and i[1] % 2 == 0) or (i[0] % 2 == 1 and i[1] % 2 == 1):
                surface.blit(self.green_1, (i[0] * SIZE, i[1] * SIZE))
            else:
                surface.blit(self.green_2, (i[0] * SIZE, i[1] * SIZE))

    def count_on_grass(self, snake):
        count = 0
        for i in snake:
            if [i[0] // SIZE, i[1] // SIZE] in self.pos:
                count += 1
        return count


class Sand:
    def __init__(self, all_pos):
        pos = []
        for i in range(RES // SIZE):
            for j in range(RES // SIZE):
                if all_pos[i][j] == 3:
                    pos.append([j, i])
        self.pos = pos
        self.rose_1 = ROSE_ONE.convert_alpha()
        self.rose_2 = ROSE_TWO.convert_alpha()

    def draw(self):
        for i in self.pos:
            if (i[0] % 2 == 0 and i[1] % 2 == 0) or (i[0] % 2 == 1 and i[1] % 2 == 1):
                surface.blit(self.rose_1, (i[0] * SIZE, i[1] * SIZE))
            else:
                surface.blit(self.rose_2, (i[0] * SIZE, i[1] * SIZE))

    def count_on_sand(self, snake):
        count = 0
        for i in snake:
            if [i[0] // SIZE, i[1] // SIZE] in self.pos:
                count += 1
        return count


class Apple:
    def __init__(self, rocks):
        x = randrange(SIZE, RES - SIZE, SIZE)
        y = randrange(SIZE, RES - SIZE, SIZE)
        while rocks.in_rock(x // SIZE, y // SIZE):
            x = randrange(SIZE, RES - SIZE, SIZE)
            y = randrange(SIZE, RES - SIZE, SIZE)
        self.x = x
        self.y = y
        self.size = SIZE

    def draw(self):
        surface.blit(APPLE_IMG, self.x, self.y)


class Freeze:
    def __init__(self, rocks, power=randrange(20, int((score * 20 + 180) / 2))):
        self.power = power
        x = randrange(SIZE, RES - SIZE, SIZE)
        y = randrange(SIZE, RES - SIZE, SIZE)
        while rocks.in_rock(x // SIZE, y // SIZE):
            x = randrange(SIZE, RES - SIZE, SIZE)
            y = randrange(SIZE, RES - SIZE, SIZE)
        self.x = x
        self.y = y
        self.size = SIZE

    def draw(self):
        surface.blit(FREEZE_IMG, (self.x, self.y))


class FreezeApple(Freeze):
    def __init__(self, rocks):
        super().__init__(rocks)
        self.fr_apple = FREEZE_APPLE.convert_alpha()

    def draw(self):
        surface.blit(self.fr_apple, (self.x, self.y))


class GoldenApple(Freeze):
    def __init__(self, rocks):
        super().__init__(rocks)
        self.gl_apple = GOLDEN_APPLE.convert_alpha()

    def draw(self):
        surface.blit(self.gl_apple, (self.x, self.y))


def level_menu():
    while choose_level():
        pass


def choose_theme():
    global back
    theme1 = Button(185, 70)
    theme2 = Button(185, 70)
    theme3 = Button(185, 70)
    while True:
        close_game()
        surface.blit(MENU_BKCGR, (0, 0))

        if theme1.draw(290, 200, 'Theme 1', font_size=50):
            back = BACK1
            return
        if theme2.draw(290, 300, 'Theme 2', font_size=50):
            back = BACK2
            return
        if theme3.draw(290, 400, 'Theme 3', font_size=50):
            back = BACK3
            return
        pygame.display.update()
        clock.tick(60)


def choose_level():
    global level
    level1 = Button(160, 70)
    level2 = Button(160, 70)
    level3 = Button(160, 70)
    level4 = Button(160, 70)
    level5 = Button(160, 70)
    while True:
        close_game()

        surface.blit(MENU_BKCGR, (0, 0))
        print_text('Press Esc to exit.', 40, 50)
        if level1.draw(320, 200, 'Level 1', font_size=50):
            level = maps[0]
            return
        if level2.draw(320, 300, 'Level 2', font_size=50):
            level = maps[1]
            return
        if level3.draw(320, 400, 'Level 3', font_size=50):
            level = maps[2]
            return
        if level4.draw(320, 500, 'Level 4', font_size=50):
            level = maps[3]
            return
        if level5.draw(320, 600, 'Level 5', font_size=50):
            level = maps[4]
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        # clock.tick(60)


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
