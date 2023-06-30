"""An implementation of simple snake game using reinforcement learning"""
__author__ = "Joao Joseph Baeta"
__author__ = "Jordan Ayiku Teye"


import torch
import random
import numpy as np
from collections import deque
from Snake import Game
from model import Linear_QNet, QTrainer
from helper import plot

max_memory = 100_000
batch_size = 1000

LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # exploitation vs exploration
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=max_memory)
        self.model = Linear_QNet(11, 256, 3) #(State, model, action)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        


    def get_state(self, game):
        head_x = game.snake.block_x[0]
        head_y = game.snake.block_y[0]
        apple_x = game.apple.apple_x
        apple_y = game.apple.apple_y

        up_step = head_y - 40
        down_step = head_y + 40
        left_step = head_x - 40
        right_step = head_x + 40
        
        dir_r = game.snake.direction == 'right'
        dir_l = game.snake.direction == 'left'
        dir_u = game.snake.direction == 'up'
        dir_d = game.snake.direction == 'down'           

        state = [


            # Danger straight
            (dir_r and game.potential_collision(right_step, head_y)) or
            (dir_l and game.potential_collision(left_step, head_y)) or
            (dir_u and game.potential_collision(head_x, up_step))or
            (dir_d and game.potential_collision(head_x, down_step)),

            # Danger right
            (dir_r and game.potential_collision(head_x, down_step)) or
            (dir_l and game.potential_collision(head_x, up_step)) or
            (dir_u and game.potential_collision(right_step, head_y))or
            (dir_d and game.potential_collision(left_step, head_y)),

            # Danger left
            (dir_r and game.potential_collision(head_x, up_step)) or
            (dir_l and game.potential_collision(head_x, down_step)) or
            (dir_u and game.potential_collision(left_step, head_y))or
            (dir_d and game.potential_collision(right_step, head_y)),

            # Move direction
            dir_u,
            dir_r,
            dir_d,
            dir_l,

            # Food location
            apple_x < head_x,  # food left
            apple_x > head_x,  # food right
            apple_y < head_y,  # food up
            apple_y > head_y  # food down
                ]

        # print(np.array(state, dtype=int))
        array = np.array(state, dtype=int)

        return array

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > batch_size:
            mini_sample = random.sample(self.memory, batch_size)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):

        # exploitation vs exploration
        self.epsilon = 120 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    record = 0
    # game_over = False
    agent = Agent()
    game = Game()
    total_score = 0
    loop_count = 0
    game.game_window.blit(game.background, (0,0))

    while True:
        loop_count += 1
        if (loop_count == 1):
            game.game_window.blit(game.background, (0,0))
            game.snake.slither()



        game.clock.tick(80)
        game.apple.draw()
        game.score_count()


        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)
        # print(state_old)

        #perform move and get new state
        reward, game_over, score, loop_count = game.take_action(final_move, loop_count)
        # game.snake.slither()
        game.game_window.blit(game.background, (0,0))
        # game.apple.draw()
        game.score_count()

        state_new = agent.get_state(game)
        # print(state_new)


        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)
        if loop_count == 500:
            game_over = True
            game.GameOver()
            agent.train_short_memory(state_old, final_move, -10, state_new, game_over)

        # remember
            agent.remember(state_old, final_move, -10, state_new, game_over)

        if game_over:
            loop_count = 0
            game.reset()

            # train long memory, plot results
            agent.train_long_memory()
            game.__init__()
            agent.n_games += 1

            if score > record:
                record = score
                # agent.model.save()

            print("Game", agent.n_games, "Score", score) # Add record

            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
