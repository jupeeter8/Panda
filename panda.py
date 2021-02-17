import pygame
import random

counter = 0


class Action:
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key





def panda(current_peice, grid):
    drop = []
    global counter
    counter += 1

    if counter == 7:
        counter = 0
        for i in range(10):
            for j in range(20):
                if grid[j][i] == (244, 243, 238):
                    continue
                else:
                    drop.append((i, j))
        if not drop:
            return []
        else:
            cords = min(drop)
            x, y = cords
            current_peice.x = x
            current_peice.y = y
            drop = []
            return []
    else:
        return []


'''key_press = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s]


def ai_run():
    global counter
    counter += 1
    if counter == 10:
        counter = 0
        z = random.choice(key_press)
        e = Action(pygame.KEYDOWN, z)
        return [e]

    else:
        return []'''
