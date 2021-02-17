import pygame
import random
import panda

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

game_window_x = 300
game_window_y = 600
origin_x = 150
origin_y = 100
green = (135, 186, 110)
blue = (54, 94, 125)
bs = 30

width, height = 1300, 800  # size of window
running = True
pygame.init()  # initialization
load_Image = pygame.image.load(r"load.png")  # load image
screen = pygame.display.set_mode((width, height))  # making screen object
game_mode = 0  # default game mode
shapes = [S, J, I, L, O, Z, T]
shape_colors = [(183, 153, 13), (89, 89, 74), (163, 165, 195), (252, 81, 48), (255, 165, 0), (15, 113, 115),
                (128, 0, 128)]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shape_colors[shapes.index(shape)]
        self.rotation = random.randint(0, len(shape))


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def convert_shape_format(shape):
    positions = []
    order = shape.shape[shape.rotation % len(shape.shape)]  # to get the rotation of the piece

    for i, line in enumerate(order):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # to offset the piece while drawing
    return positions


def valid(shape, grid):
    acc_pos = [[(j, i) for j in range(10) if grid[i][j] == (244, 243, 238)] for i in range(20)]
    acc_pos = [j for sub in acc_pos for j in sub]  # Converting accepted positions from 2D to 1d

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in acc_pos:
            if pos[1] > -1:
                return False
    return True


def lines(start_x):
        for i in range(20):
            pygame.draw.line(screen, (214, 214, 214), (start_x, origin_y + i * bs),
                             (start_x + game_window_x, origin_y + i * bs))
        for j in range(10):
            pygame.draw.line(screen, (214, 214, 214), (start_x + j * bs, origin_y),
                             (start_x + j * bs, origin_y + game_window_y))


def row_clear(grid, lp):
    row_num = []
    for i in reversed(range(len(grid))):
        if (244, 243, 238) not in grid[i]:  # Find row with no white block
            row_num.append(i)
            for j in range(len(grid[i])):
                del lp[(i, j)]  # Delete elements in each column of that row

    for num in reversed(row_num):  # //Shifting//
        for x in reversed(range(0, num)):
            for y in range(10):
                if (x, y) in lp:
                    lp[((x + 1), y)] = lp[(x, y)]  # Copying upper row
                    del lp[(x, y)]  # Deleting upper row
                else:
                    continue
    return lp, len(row_num)


def draw_window(grid, start):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (start + j * 30, origin_y + i * 30, 30, 30), 0)
    pygame.draw.rect(screen, green, (start, origin_y, 300, 600), 4)


def box(locked_positions):
    grid = [[(244, 243, 238) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in locked_positions:  # check if coordinate already in grid
                c = locked_positions[(i, j)]  # get colour of that co-ord
                grid[i][j] = c

    return grid


def lost(positions):
    for pos in positions:  # Check vertical pos in locked pos
        x, y = pos
        if x < 1:
            return True
    return False


def draw_lost(text):
    font = pygame.font.SysFont('comic sans', 50)
    score_txt = font.render('Game Over', True, green)
    screen.blit(score_txt, (text, origin_y + 300))


def load():
    # loading screen graphics
    screen.fill((255, 255, 255))
    screen.blit(load_Image, (0, 0))
    pygame.display.set_caption("PANDA")


def ai():
    score = 0
    score_ai = 0

    locked_positions = {}
    lp_ai = {}

    change_piece = False
    change_piece_ai = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()

    cp_ai = get_shape()
    np_ai = get_shape()

    clock = pygame.time.Clock()

    fall_time = 0
    fall_speed = 0.5
    play = True
    ai_play = True

    while run:
        screen.fill(blue)
        grid = box(locked_positions)
        grid_ai = box(lp_ai)

        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 > fall_speed:
            fall_time = 0

            current_piece.y += 1

            if not valid(current_piece, grid) and current_piece.y > 0 and play:
                current_piece.y -= 1
                change_piece = True

            cp_ai.y += 1
            if not valid(cp_ai, grid_ai) and cp_ai.y and ai_play > 0:
                cp_ai.y -= 1
                change_piece_ai = True

        for event in list(pygame.event.get()) + panda.panda(cp_ai, grid_ai):
            if event.type == pygame.QUIT:
                run = False
                game_mode = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and play:
                    current_piece.y += 1
                    if not (valid(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_s and ai_play:
                    cp_ai.y += 1
                    if not (valid(cp_ai, grid_ai)):
                        cp_ai.y -= 1

                if event.key == pygame.K_UP and play:
                    current_piece.rotation += 1
                    if not (valid(current_piece, grid)):
                        current_piece.rotation -= 1

                if event.key == pygame.K_w and ai_play:
                    cp_ai.rotation += 1
                    if not (valid(cp_ai, grid_ai)):
                        cp_ai.rotation -= 1

                if event.key == pygame.K_LEFT and play:
                    current_piece.x -= 1
                    if not (valid(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_a and ai_play:
                    cp_ai.x -= 1
                    if not (valid(cp_ai, grid_ai)):
                        cp_ai.x += 1

                if event.key == pygame.K_RIGHT and play:
                    current_piece.x += 1
                    if not (valid(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_d and ai_play:
                    cp_ai.x += 1
                    if not (valid(cp_ai, grid_ai)):
                        cp_ai.x -= 1
                if event.key == pygame.K_TAB and ai_play:
                    ai_play = False

        if play:
            shape_pos = convert_shape_format(current_piece)
        else:
            shape_pos = []
        if ai_play:
            shape_pos_ai = convert_shape_format(cp_ai)
        else:
            shape_pos_ai = []

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.colour

        for i in range(len(shape_pos_ai)):
            x, y = shape_pos_ai[i]
            if y > -1:
                grid_ai[y][x] = cp_ai.colour

        draw_window(grid, origin_x)
        draw_window(grid_ai, 850)
        lines(origin_x)
        lines(850)
        if not play:
            draw_lost(210)
        if not ai_play:
            draw_lost(910)


        if change_piece and play:
            for pos in shape_pos:
                p = (pos[1], pos[0])
                locked_positions[p] = current_piece.colour
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            locked_positions, cleared = row_clear(grid, locked_positions)
            if cleared > 0:
                score += (cleared * 10) * cleared

        if change_piece_ai and ai_play:
            for pos in shape_pos_ai:
                q = (pos[1], pos[0])
                lp_ai[q] = cp_ai.colour
            cp_ai = np_ai
            np_ai = get_shape()
            change_piece_ai = False

            lp_ai, cleared_ai = row_clear(grid_ai, lp_ai)
            if cleared_ai > 0:
                score_ai += (cleared_ai * 10) * cleared_ai

        font = pygame.font.SysFont('comic sans', 30)
        score_txt = font.render('Score User : {}'.format(score), True, green)
        screen.blit(score_txt, (470, origin_y + 50))
        score_txt_ai = font.render('Score Panda : {}'.format(score_ai), True, green)
        screen.blit(score_txt_ai, (670, origin_y + 50))
        pygame.draw.line(screen, green, (650, origin_y), (650, origin_y + game_window_y), 2)
        pygame.display.set_caption("VS")
        pygame.display.update()

        if lost(locked_positions):
            play = False

        if lost(lp_ai):
            ai_play = False

        if not play and not ai_play:
            draw_lost(910)
            draw_lost(210)
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
            game_mode = 0

    return game_mode


def learn():
    score = 0
    locked_positions = {}
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()

    time_since_last_fall = 0
    how_fast_the_block_will_fall = 0.35  # block/ 0.35s
    while run:
        screen.fill(blue)
        grid = box(locked_positions)
        time_since_last_fall += clock.get_rawtime()  # Get actual time since clock.tick
        clock.tick()
        if time_since_last_fall / 1000 > how_fast_the_block_will_fall:  # If time > 0.35s move block
            time_since_last_fall = 0
            current_piece.y += 1
            # pass
            if not (valid(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in list(pygame.event.get()):  # + panda.panda(current_piece, grid):
            if event.type == pygame.QUIT:
                run = False
                game_mode = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid(current_piece, grid)):
                        current_piece.x -= 1
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):  # Draw Shape onto grid
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.colour

        draw_window(grid, 500)

        if change_piece:
            for pos in shape_pos:
                p = (pos[1], pos[0])
                locked_positions[p] = current_piece.colour  # If change piece, save current pos of grid in locked_pos
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            locked_positions, cleared = row_clear(grid, locked_positions)
            if cleared > 0:
                score += (cleared * 10) * cleared
        font = pygame.font.SysFont('comic sans', 30)
        score_txt = font.render('Score : {}'.format(score), True, green)
        screen.blit(score_txt, (600, 20))
        pygame.display.set_caption("LEARN")
        pygame.display.update()

        if lost(locked_positions):  # Check if game is lost
            draw_lost(560)
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
            game_mode = 0

    return game_mode


while running:

    if game_mode == 0:
        load()
    elif game_mode == 1:
        game_mode = learn()  # Alternate between game modes
    elif game_mode == 2:
        game_mode = ai()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game_mode = 1

            if event.key == pygame.K_p:
                game_mode = 2

            if event.key == pygame.K_ESCAPE:
                game_mode = 0

    pygame.display.flip()
pygame.display.quit()
