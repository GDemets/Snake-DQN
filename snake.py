import random
import numpy as np
import gymnasium as gym


class SnakeEnv(gym.Env):
    def __init__(self):
        self.row=20
        self.col=20
        self.state=np.zeros((self.row,self.col))
        self.snake=[[5,5]]
        self.state[self.snake[0][0],self.snake[0][1]]=1
        self.score=0
        self.alive=True
        self.directions = [(-1,0), (0,1), (1,0), (0,-1)] # Up, Right, Down, Left
        self.direction=0
        self.food=[]
        self.place_food()
        
        ### Gym setups ###
        self.observation_space = gym.spaces.Box(
            low=0, high=2,
            shape=(self.row * self.col,),
            dtype=np.int32
        ) # observation space

        self.action_space = gym.spaces.Discrete(4) # action space: 4 directions
    
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
        
        ### check impossible movement ###
        if self.direction==0 and action==2:
            action = self.direction
        if self.direction==1 and action ==3:
            action=self.direction
        if self.direction==2 and action ==0:
            action=self.direction
        if self.direction==3 and action ==1:
            action=self.direction

        new_head = [self.snake[0][0] + x, self.snake[0][1] + y]

        ### check collisions ###
        if new_head[0] < 0 or new_head[0] >= self.row or new_head[1] < 0 or new_head[1] >= self.col: # check wall collision
            self.alive = False
            reward-=10
            info = {}
            truncated=not self.alive
            terminated=False
            return self.state.flatten(), reward, terminated, truncated, info
        if new_head in self.snake: # check self-collision
            self.alive = False
            reward-=10
            info = {}
            truncated=not self.alive
            terminated=False
            return self.state.flatten(), reward, terminated, truncated, info

        if new_head in self.food: # check food collision
            self.snake.insert(0, new_head)
            self.food.remove(new_head)
            self.score += 1
            reward += 10
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

        info = {}
        truncated=not self.alive
        terminated=False

        return self.state.flatten(), reward, terminated, truncated, info # return state, reward, done, info
            
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
        return self.state.flatten(), {"score": self.score}

    
