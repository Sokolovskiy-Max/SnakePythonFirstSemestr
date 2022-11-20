from random import randrange
from parameters import *
from Button import Button
from save import *
from highscore import *
from Maps import maps

pygame.init()

save_data = Saves()
high_scores = HighScores(save_data.get('hs'))
print(save_data.add('hs', {}))

score = 0
back = pygame.image.load('theme1.jpg')
level = maps[0]


def game_circle():
    global score

    game = True

    grass = Grass(level)
    sand = Sand(level)
    rocks = Rocks(level)

    apple = Apple(rocks)
    fr_apple = FreezeApple(rocks)
    golden_apple = GoldenApple(rocks)
    length = 1
    x, y = find_spawn(level)
    snake = [(x, y)]
    dx, dy = 0, 0
    tail_dx, tail_dy = 0, 0
    fps = 180
    dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
    score = 0
    speed_count, snake_speed = 0, 1
    pygame.init()
    font_score = pygame.font.SysFont('font.oTF', 50, bold=True)
    tdx = 0
    tdy = 0
    freeze = Freeze(rocks)
    freeze_exist = 0
    freeze_apple_exist = 0
    golden_apple_exist = 0
    k = 0
    while game:
        surface.blit(back, (0, 0))

        grass.draw()
        sand.draw()
        rocks.draw()
        if (dx, dy) == (0, 0):
            [pygame.draw.rect(surface, pygame.Color('orange'), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
        if freeze_exist:
            surface.blit(freeze_img, (freeze.x, freeze.y, SIZE, SIZE))

        # apple.draw()
        surface.blit(apple_img, (apple.x, apple.y, SIZE, SIZE))
        if freeze_apple_exist:
            fr_apple.draw()
        if golden_apple_exist:
            golden_apple.draw()
        # show score
        render_score = font_score.render(f'SCORE: {score}', True, pygame.Color('orange'))
        surface.blit(render_score, (5, 5))
        key = pygame.key.get_pressed()
        if dx == tdx and dy == tdy:
            if key[pygame.K_w]:
                if dirs['W']:
                    tdx, tdy = 0, -1
                    dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
            elif key[pygame.K_s]:
                if dirs['S']:
                    tdx, tdy = 0, 1
                    dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
            elif key[pygame.K_a]:
                if dirs['A']:
                    tdx, tdy = -1, 0
                    dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
            elif key[pygame.K_d]:
                if dirs['D']:
                    tdx, tdy = 1, 0
                    dirs = {'W': True, 'S': True, 'A': False, 'D': True, }
        if dx == 1:
            pygame.draw.rect(surface, pygame.Color('orange'), (snake[-1][0] - 1, snake[-1][1], k, SIZE - 1))
        if dx == -1:
            pygame.draw.rect(surface, pygame.Color('orange'), (snake[-1][0] + SIZE - k, snake[-1][1], k, SIZE - 1))
        if dy == 1:
            pygame.draw.rect(surface, pygame.Color('orange'), (snake[-1][0], snake[-1][1], SIZE - 1, k))
        if dy == -1:
            pygame.draw.rect(surface, pygame.Color('orange'), (snake[-1][0], snake[-1][1] + SIZE - k, SIZE - 1, k))
        if tail_dx == 1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (snake[0][0] + k - SIZE, snake[0][1], SIZE - 1 - k, SIZE - 1))
        if tail_dy == 1:
            pygame.draw.rect(surface, pygame.Color('orange'),
                             (snake[0][0], snake[0][1] + k - SIZE, SIZE - 1, SIZE - k))
        if tail_dx == -1:
            pygame.draw.rect(surface, pygame.Color('orange'), (snake[0][0] + SIZE, snake[0][1], SIZE - k, SIZE - 1))
        if tail_dy == -1:
            pygame.draw.rect(surface, pygame.Color('orange'), (snake[0][0], snake[0][1] + SIZE, SIZE - 1, SIZE - k))

        [pygame.draw.rect(surface, pygame.Color('orange'), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake[:-1]]
        pygame.display.flip()
        clock.tick(
            fps * (1 + grass.count_on_grass(snake) / length) * (1 - 0.5 * sand.count_on_sand(snake) / length))
        surface.blit(back, (0, 0))
        k += 1

        if k == SIZE:
            dx, dy = tdx, tdy
            if len(snake) > 1:
                if snake[0][0] > snake[1][0]:
                    tail_dx = -1
                    tail_dy = 0
                elif snake[0][0] < snake[1][0]:
                    tail_dx = 1
                    tail_dy = 0
                elif snake[0][1] > snake[1][1]:
                    tail_dy = -1
                    tail_dx = 0
                elif snake[0][1] < snake[1][1]:
                    tail_dy = 1
                    tail_dx = 0
            else:
                tail_dx, tail_dy = dx, dy
            render_score = font_score.render(f'SCORE: {score}', True, pygame.Color('orange'))
            surface.blit(render_score, (5, 5))
            if freeze_exist == 0:
                if 1 // randrange(1, 250):
                    freeze = Freeze(rocks)
                    freeze_exist = 1
            if freeze_apple_exist == 0:
                if 1 // randrange(1, 250):
                    fr_apple = FreezeApple(rocks)
                    freeze_apple_exist = 1
            if golden_apple_exist == 0:
                if 1 // randrange(1, 500):
                    golden_apple = GoldenApple(rocks)
                    golden_apple_exist = 1
            x += dx * SIZE
            y += dy * SIZE
            snake.append((x, y))
            snake = snake[-length:]
            speed_count += 1
            k = 0
        if snake[-1] == (apple.x, apple.y):
            pygame.mixer.Sound.play(eat_sound)
            apple = Apple(rocks)
            surface.blit(apple_img, (apple.x, apple.y, SIZE, SIZE))
            length += 1
            score += 1
            fps += 20
        if freeze_apple_exist == 1 and snake[-1] == (fr_apple.x, fr_apple.y):
            pygame.mixer.Sound.play(eat_sound)
            score += 1
            length += 4
            fps -= fr_apple.power
            freeze_apple_exist = 0
        if freeze_exist == 1 and snake[-1] == (freeze.x, freeze.y):
            pygame.mixer.Sound.play(eat_sound)
            score -= 2
            fps -= freeze.power
            freeze_exist = 0
        if golden_apple_exist == 1 and snake[-1] == (golden_apple.x, golden_apple.y):
            pygame.mixer.Sound.play(eat_sound)
            score += 5
            length += 5
            golden_apple_exist = 0

        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            game = False
        if any((i[0] * SIZE, i[1] * SIZE) == snake[-1] for i in rocks.pos):
            game = False
        close_game()
    print(freeze_apple_exist)
    return game_over()


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
                print(name)
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
        # clock.tick(15)


def find_spawn(level):
    for i in range(RES // SIZE):
        for j in range(RES // SIZE):
            if level[i][j] == 5:
                return j * SIZE, i * SIZE


def start_game():
    choose_theme()
    while game_circle():
        pass


def show_menu():
    start_btn = Button(254, 70)
    level_btn = Button(120, 70)
    quit_btn = Button(108, 70)

    start_btn.draw(148, 270, 'Srart game', start_game, 50)
    level_btn.draw(328, 400, 'Level', level_menu, 50)
    quit_btn.draw(508, 530, 'Quit', quit, 50)

    show = True

    while show:
        close_game()

        surface.blit(menu_bkcgr, (0, 0))

        start_btn.draw(280, 270, 'Srart game', start_game, 50)
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
        self.rock_png = pygame.image.load('rock.png').convert_alpha()
        self.rock_1 = pygame.image.load('rock_1.png').convert_alpha()
        self.rock_2 = pygame.image.load('rock_2.png').convert_alpha()

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
        self.green_1 = pygame.image.load('green_1.png').convert_alpha()
        self.green_2 = pygame.image.load('green_2.png').convert_alpha()

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
        self.rose_1 = pygame.image.load('rose_1.png').convert_alpha()
        self.rose_2 = pygame.image.load('rose_2.png').convert_alpha()

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
        surface.blit(apple_img, self.x, self.y)


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
        surface.blit(freeze_img, (self.x, self.y))


class FreezeApple(Freeze):
    def __init__(self, rocks):
        super().__init__(rocks)
        self.fr_apple = pygame.image.load('freeze_apple.png').convert_alpha()

    def draw(self):
        surface.blit(self.fr_apple, (self.x, self.y))


class GoldenApple(Freeze):
    def __init__(self, rocks):
        super().__init__(rocks)
        self.gl_apple = pygame.image.load('golden_apple.png').convert_alpha()

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
        surface.blit(menu_bkcgr, (0, 0))

        if theme1.draw(290, 200, 'Theme 1', font_size=50):
            back = back1
            return
        if theme2.draw(290, 300, 'Theme 2', font_size=50):
            back = back2
            return
        if theme3.draw(290, 400, 'Theme 3', font_size=50):
            back = back3
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

        surface.blit(menu_bkcgr, (0, 0))
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


show_menu()
pygame.quit()
quit()
