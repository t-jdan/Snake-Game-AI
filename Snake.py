"""An implementation of simple snake game using reinforcement learning"""
__author__ = "Joao Joseph Baeta"
__author__ = "Jordan Ayiku Teye"

import pygame
from pygame.locals import *  # imports global variables form pygame module
from pygame import mixer
import time
import random
import numpy as np

block_size = 40
class Apple:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.apple = pygame.image.load('apple2.png')
        self.apple_x = random.randint(45, 890)
        self.apple_y = random.randint(45, 750)

    def draw(self):
        self.parent_window.blit(self.apple, (self.apple_x, self.apple_y))
        pygame.display.flip()  # To show the block

    def Spawn_position(self):
        self.apple_x = random.randint(45, 890)
        self.apple_y = random.randint(45, 750)

class Snake:
    def __init__(self, parent_window, length):
        self.parent_window = parent_window
        self.length = length
        self.block = pygame.image.load('snake_body2.png')
        self.block_x = [400] * length  # Defining the block x location
        self.block_y = [280] * length  # Defining the block y location
        self.direction = 'right'

    # Function that draws the snake
    def draw(self):
        for i in range(self.length):
            self.parent_window.blit(self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.flip()  # To show the block

    def increase_size(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)


    # # Function that moves the snake Up
    # def Move_Up(self):
    #     self.direction = 'up'

    # # Function that moves the snake down
    # def Move_Down(self):
    #     self.direction = 'down'

    # # Function that moves the snake to the left
    # def Move_Left(self):
    #     self.direction = 'left'

    # # Function that moves the snake to the right
    # def Move_Right(self):
    #     self.direction = 'right'

    # Function that gets the snake to move by itself
    def slither(self):
        for i in range(self.length - 1, 0, -1):
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]

        if (self.direction == 'up'):
            self.block_y[0] -= block_size
        elif (self.direction == 'down'):
            self.block_y[0] += block_size
        elif (self.direction == 'left'):
            self.block_x[0] -= block_size
        elif (self.direction == 'right'):
            self.block_x[0] += block_size

        self.draw()


class Game():
    # Defining colors
    green = pygame.Color(0, 255, 0)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    blue = pygame.Color(0, 0, 255)
    yellow = pygame.Color(255, 255, 0)

    def __init__(self):
        pygame.init()

        self.reward = 0
        self.score = 0

        # Defining the window size
        self.window_x = 1000
        self.window_y = 800

        # Storing the background picture of the game
        self.background = pygame.image.load('BG.png')

        # Initialising game window
        pygame.display.set_caption('Simple Snake Game')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.game_window.blit(self.background, (0, 0))

        self.snake = Snake(self.game_window, 2)
        self.snake.draw()
        self.apple = Apple(self.game_window)
        self.apple.draw()
        self.clock = pygame.time.Clock()

    def GameOver(self):
        # self.game_window.blit(self.background, (0, 0))
        # font = pygame.font.SysFont('arial', 45)
        # font2 = pygame.font.SysFont('arial', 30)
        # Game_Over = font.render(f"GAME OVER",True, (255, 0, 0))
        # score = font2.render(f"Your score was  {(self.snake.length * 10) - 10}", True, (255, 0, 0))
        # text=font2.render(f"To play again,press the ENTER key and to quit, press the ESC key",True, (255, 0, 0))
        # self.game_window.blit(Game_Over, (390,300))
        # self.game_window.blit(score, (400, 400))
        # self.game_window.blit(text, (115, 490))
        pygame.display.flip()                  #helps to bassically refresh the UI
        self.reward = -10


    def hasbeeneaten(self, x1, y1, x2, y2):
        if (x1 >= x2 and x1 < x2 + block_size):
            if (y1 >= y2 and y1 < y2 + block_size):
                return True
        elif(x1 <= x2 and x1 > x2 - block_size):
            if (y1 <= y2 and y1 > y2 - block_size):
                return True
        else:
            return False

    def out_of_bounds(self, x1, y1, x2, y2):
        if (x1 >= x2 and x1 < x2 + block_size):
            if (y1 >= y2 and y1 < y2 + block_size):
                return True
        elif (x1 <= x2 and x1 > x2 - block_size):
            if (y1 <= y2 and y1 > y2 - block_size):
                return True
        else:
            return False

    def score_count(self):
        font=pygame.font.SysFont('arial',30)
        score = font.render(f"Score:  {(self.snake.length *10) - 20}", True, (0, 0, 255))
        self.game_window.blit(score,(850,5))

    def reset(self):
        self.game_window.blit(self.background, (0,0))
        self.snake = Snake(self.game_window, 2)
        self.snake.draw()
        self.apple = Apple(self.game_window)
        self.apple.draw()

    def step(self, action):

        clock_wise = ['right', 'down', 'left', 'up']
        idx = clock_wise.index(self.snake.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # go straight
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # turn right
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # turn left

        return new_dir

    def apple_eaten(self):
        # Increases the size of the snake by one block if it eats an apple
        if self.hasbeeneaten(self.snake.block_x[0], self.snake.block_y[0], self.apple.apple_x, self.apple.apple_y):
            self.snake.increase_size()
            self.apple.Spawn_position()
            return True
        return False


    # checks danger states
    def potential_collision(self, x_value, y_value):
        self.some_collision = False

        # eats itself
        for i in range(2, self.snake.length):
            if self.hasbeeneaten(x_value, y_value, self.snake.block_x[i], self.snake.block_y[i]):
                self.some_collision = True

        # hits upper and lower boundary
        if self.out_of_bounds(x_value, y_value, x_value, -40) or self.out_of_bounds(x_value, y_value, x_value, self.window_y):
            self.some_collision = True
            # print("Error at upper or lower bound")

        # hits left and right boundary
        if self.out_of_bounds(x_value, y_value, -block_size, y_value) or self.out_of_bounds(x_value, y_value, self.window_x, y_value):
            self.some_collision = True
            # print("Error at side")

        return self.some_collision

    def is_collision(self):
        self.collision = False

        #Checks to see if snake has eaten itself
        for i in range(1,self.snake.length):
            if self.hasbeeneaten(self.snake.block_x[0], self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i]):
                self.collision = True

        #Checks to see if snake hits the boundaries of the window
        # For Upper and lower boundaries

        if self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[0], 0) or self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[0], self.window_y):
            self.collision = True

        # #For Side boundaries
        if self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0], 0, self.snake.block_y[0]) or self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0],self.window_x, self.snake.block_y[0]):
            self.collision = True

        return self.collision


    def take_action(self, action, loop_count):
        self.game_over = False
        self.reward = 0
        loop_count = loop_count


        self.snake.direction = self.step(action)
        self.snake.slither()
        # self.game_window.blit(self.background, (0,0))

        if(self.apple_eaten()):
                self.score += 10
                self.reward = 10
                loop_count = 0
        if(self.is_collision()):
            self.pause = True
            self.game_over = True
            self.GameOver()

        # print("Reward: ", self.reward)
        return self.reward, self.game_over, self.score, loop_count

