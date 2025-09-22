import random
import numpy as np
import gymnasium as gym
import math


class SnakeEnv(gym.Env):
    def __init__(self):
        self.row = 5
        self.col = 5
        self.state = np.zeros((self.row, self.col))
        self.snake = [[2, 2]]  # initial position of the snake
        self.state[self.snake[0][0], self.snake[0][1]] = 1
        self.score = 0
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
        self.direction = 0
        self.food = []
        self.place_food(1)
        self.truncated = False  # If no more space to place food
        self.terminated = False  # False : snake alive / True : snake dead
        self.info = {}

        ### Gym setups ###
        self.observation_space = gym.spaces.Box(
            low=0, high=2, shape=(self.row * self.col,), dtype=np.float32
        )  # observation space : grid (row * col)

        self.action_space = gym.spaces.Discrete(4)  # action space: 4 directions

    def place_food(self, num_food=1):
        empty_space = []
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    empty_space.append([i, j])

        for i in range(num_food):
            if len(empty_space) == 0:
                self.truncated = True
                return
            else:
                food = random.choice(empty_space)
                self.food.append(food)
                self.state[food[0], food[1]] = 2

    def step(self, action):
        reward = 0.0
        old_head = self.snake[0]

        ### check impossible movement ###
        if self.direction == 0 and action == 2:
            action = self.direction
        if self.direction == 1 and action == 3:
            action = self.direction
        if self.direction == 2 and action == 0:
            action = self.direction
        if self.direction == 3 and action == 1:
            action = self.direction

        ### get the new head psoition ###
        x, y = self.directions[action]
        new_head = [self.snake[0][0] + x, self.snake[0][1] + y]

        ### check collisions ###
        if (
            new_head[0] < 0
            or new_head[0] >= self.row
            or new_head[1] < 0
            or new_head[1] >= self.col
        ):  # check wall collision
            reward -= 10
            self.terminated = True
            return (
                self.state.flatten(),
                reward,
                self.terminated,
                self.truncated,
                self.info,
            )

        if new_head in self.snake:  # check self-collision
            reward -= 10
            self.terminated = True
            return (
                self.state.flatten(),
                reward,
                self.terminated,
                self.truncated,
                self.info,
            )

        if new_head in self.food:  # check food collision
            self.snake.insert(0, new_head)
            self.food.remove(new_head)
            self.score += 1
            reward = reward + 15 + self.score
            self.place_food(1)  # place new food
        else:  # move forward
            self.snake.insert(0, new_head)  # add head at new position
            self.snake.pop()  # remove the last one

        ### calculate reward ###
        old_distance = abs(old_head[0] - self.food[0][0]) + abs(
            old_head[1] - self.food[0][1]
        )
        new_distance = abs(new_head[0] - self.food[0][0]) + abs(
            new_head[1] - self.food[0][1]
        )
        if new_distance < old_distance:
            reward += 0.1
        else:
            reward -= 0.05

        ### update state ###
        self.state = np.zeros((self.row, self.col))  # reset the field
        for x, y in self.snake:
            self.state[x, y] = 1  # mark the snake's body
        for fx, fy in self.food:
            self.state[fx, fy] = 2  # mark the food's position

        self.direction = action  # update the direction
        # reward += 0.05  # small reward for staying alive

        return (
            self.state.flatten().astype(np.float32),
            reward,
            self.terminated,
            self.truncated,
            self.info,
        )  # return state, reward, terminated : end by death, truncated : natural end, info

    def render(self):
        print("Score : ", self.score)
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    print(".", end=" ")
                elif self.state[i][j] == 1:
                    print("S", end=" ")
                elif self.state[i][j] == 2:
                    print("F", end=" ")

    def reset(self):
        self.state = np.zeros((self.row, self.col))
        self.snake = [[2, 2]]
        self.state[self.snake[0][0], self.snake[0][1]] = 1
        self.direction = 0
        self.score = 0
        self.alive = True
        self.food = []
        self.place_food(1)
        self.truncated = False
        self.terminated = False
        self.info = {}
        return self.state.flatten().astype(np.float32), self.info
