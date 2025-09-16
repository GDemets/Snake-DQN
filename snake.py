import random
import numpy as np
import gymnasium as gym


class SnakeEnv():
    def __init__(self):
        self.row=20
        self.col=20
        self.state=np.zeros((self.row,self.col))
        self.snake=[[5,5]]
        self.state[self.snake[0][0],self.snake[0][1]]=1
        self.direction=0
        self.score=0
        self.alive=True
        self.directions = [(-1,0), (0,1), (1,0), (0,-1)] # Up, Right, Down, Left
        self.food=[]
        self.place_food()
    
    def place_food(self, num_food=1):
        for i in range(num_food):
            while True:
                food=[random.randint(0,self.row-1),random.randint(0,self.col-1)]
                if self.state[food[0],food[1]]==0:
                    self.food.append(food)
                    self.state[food[0],food[1]]=2
                    break

    def step(self, action):
        reward = -0.1
        x, y = self.directions[action]
        new_head = [self.snake[0][0] + x, self.snake[0][1] + y]

        ### check collisions ###
        if new_head[0] < 0 or new_head[0] >= self.row or new_head[1] < 0 or new_head[1] >= self.col: # check wall collision
            self.alive = False
            return self.state, -100, self.alive
        if new_head in self.snake: # check self-collision
            self.alive = False
            return self.state, -100, self.alive

        if new_head in self.food: # check food collision
            self.snake.insert(0, new_head)
            self.food.pop(new_head)
            self.score += 1
            reward += 50
            self.place_food(1) # place new food
        else : # move forward
            self.snake.insert(0, new_head) # add head at new position
            self.snake.pop() # remove the last one 
        
        ### update state ###
        self.state = np.zeros((self.row, self.col)) # reset the field
        for x, y in self.snake:
            self.state[x, y] = 1 # mark the snake's body
        for fx,fy in self.food:
            self.state[fx, fy] = 2  #mark the food's position

        return self.state, reward, not self.alive # return state, reward, done
            
    def render(self):
        pass
    
    def reset(self):
        self.state = np.zeros((self.row, self.col))
        self.snake = [[5, 5]]
        self.state[5, 5] = 1
        self.direction = 0
        self.score = 0
        self.alive = True
        self.food = []
        self.place_food()
        return self.state