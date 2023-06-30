"""An implementation of simple snake game using reinforcement learning"""
__author__ = "Joao Joseph Baeta"
__author__ = "Jordan Ayiku Teye"

import pygame
from pygame.locals import *  # imports global variables form pygame module
from pygame import mixer
import time
import random
from enum import Enum

block_size = 40
class Apple:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.apple = pygame.image.load('apple2.png')
        self.apple_x = random.randint(0, 965)
        self.apple_y = random.randint(0, 730)

    def draw(self):
        self.parent_window.blit(self.apple, (self.apple_x, self.apple_y))
        pygame.display.flip()  # To show the block

    def Spawn_position(self, event):
        self.apple_x = random.randint(0, 965)
        self.apple_y = random.randint(0, 730)

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Snake:
    def __init__(self, parent_window, length):
        self.parent_window = parent_window
        self.length = length
        self.block = pygame.image.load('snake_body2.png')
        self.block_x = [block_size] * length  # Defining the block x location
        self.block_y = [block_size] * length  # Defining the block y location
        self.direction = Direction.RIGHT

    # Function that draws the snake
    def draw(self):
        for i in range(self.length):
            self.parent_window.blit(self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.flip()  # To show the block

    #Function that increases the size of the snake
    def increase_size(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    # Function that moves the snake Up
    def Move_Up(self):
        self.direction = Direction.UP

    # Function that moves the snake down
    def Move_Down(self):
        self.direction = Direction.DOWN

    # Function that moves the snake to the left
    def Move_Left(self):
        self.direction = Direction.LEFT

    # Function that moves the snake to the right
    def Move_Right(self):
        self.direction = Direction.RIGHT

    # Function that gets the snake to move by itself
    def slither(self):
        for i in range(self.length - 1, 0, -1):
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]

        if (self.direction == Direction.UP):
            self.block_y[0] -= block_size
        elif (self.direction == Direction.DOWN):
            self.block_y[0] += block_size
        elif (self.direction == Direction.LEFT):
            self.block_x[0] -= block_size
        elif (self.direction == Direction.RIGHT):
            self.block_x[0] += block_size

        self.draw()


class Game:
    # Defining colors
    green = pygame.Color(0, 255, 0)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    blue = pygame.Color(0, 0, 255)
    yellow = pygame.Color(255, 255, 0)

    def __init__(self):
        pygame.init()

        # Defining the window size
        self.window_x = 800
        self.window_y = 600

        # Storing the background picture of the game
        self.background = pygame.image.load('BG.png')

        # Initialising game window
        pygame.display.set_caption('Simple Snake Game')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.game_window.blit(self.background, (0, 0))
        # game_window.fill(blue)              # Changing the surface color

        self.snake = Snake(self.game_window, 2)
        self.snake.draw()
        self.apple = Apple(self.game_window)
        self.apple.draw()

    def GameOver(self):
        self.game_window.blit(self.background, (0, 0))
        font = pygame.font.SysFont('arial', 45)
        font2 = pygame.font.SysFont('arial', 30)
        Game_Over = font.render(f"GAME OVER",True, (255, 0, 0))
        score = font2.render(f"Your score was {(self.snake.length * 10) - 10}", True, (255, 0, 0))
        text=font2.render(f"To play again,press the ENTER key and to quit, press the ESC key",True, (255, 0, 0))
        self.game_window.blit(Game_Over, (390,300))
        self.game_window.blit(score, (400, 400))
        self.game_window.blit(text, (120, 490))
        pygame.display.flip()                  #helps to bassically refresh the UI



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
        score= font.render(f"Score:  {(self.snake.length *10) - 20}", True, (0, 0, 255))
        self.game_window.blit(score,(850,5))

    def reset(self):
        self.snake = Snake(self.game_window, 2)
        self.snake.draw()
        self.apple = Apple(self.game_window)
        self.apple.draw()

    def run(self):
        # pygame.mixer.init()
        # pygame.mixer.music.load('bgmusic.mp3')
        # pygame.mixer.music.play()
        running = True
        pause = False
        while running:
            self.game_window.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if (event.type == KEYDOWN):
                    if event.key == K_RETURN:
                        pause = False
                        self.reset()
                    if event.key == K_ESCAPE:
                        running = False
                    if (event.key == K_UP):
                        self.snake.Move_Up()
                    if (event.key == K_DOWN):
                        self.snake.Move_Down()
                    if (event.key == K_LEFT):
                        self.snake.Move_Left()
                    if (event.key == K_RIGHT):
                        self.snake.Move_Right()

                elif (event.type == pygame.QUIT):
                    running = False



            if not pause:
                self.snake.slither()
                self.apple.draw()
                self.score_count()
                pygame.display.flip()

            # Increases the size of the snake by one block if it eats an apple
            if self.hasbeeneaten(self.snake.block_x[0], self.snake.block_y[0], self.apple.apple_x, self.apple.apple_y):
                self.snake.increase_size()
                self.apple.Spawn_position(event)

            #Checks to see if snake has eaten itself
            for i in range(1,self.snake.length):
                if self.hasbeeneaten(self.snake.block_x[0], self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i]):
                        self.GameOver()
                        pause = True

            #Checks to see if snake hits the boundaries of the window
            # For Upper and lower boundaries
            
            if self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[0], -20) or self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[0], self.window_y):
                self.GameOver()
                pause = True

        # #For Side boundaries
            if self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0], -block_size, self.snake.block_y[0]) or self.out_of_bounds(self.snake.block_x[0], self.snake.block_y[0],self.window_x, self.snake.block_y[0]):
                self.GameOver()
                pause = True



            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()
