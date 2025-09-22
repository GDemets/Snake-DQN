import pygame
import torch
from DQN import DQN
from snake import SnakeEnv

### Color setup ###
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

### Load trained model ###
model = DQN(n_observations=25, n_actions=4)
state_dict = torch.load("models/snake_dqn2.pth", map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

### Environment setup ###
env = SnakeEnv()

### Pygame setups ###
pygame.init()
cell_size = 40
width, height = env.col * cell_size, (1 + env.row) * cell_size
clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DQN Snake")
font = pygame.font.SysFont(None, 30)

### Main loop ###
state, info = env.reset()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if env.terminated or env.truncated:
        state, info = env.reset()

    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    q_values = model(state_tensor)
    action = q_values.argmax(dim=1).item()
    next_state, reward, terminated, truncated, _ = env.step(action)
    state = next_state

    win.fill(BLACK)
    for i in range(env.row):
        for j in range(env.col):
            if env.state[i][j] == 1:  # Snake
                pygame.draw.rect(
                    win, GREEN, (j * cell_size, i * cell_size, cell_size, cell_size)
                )
            elif env.state[i][j] == 2:  # Food
                pygame.draw.circle(
                    win,
                    RED,
                    (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
                    cell_size // 2,
                )

    score_text = font.render(f"Score: {env.score}", True, WHITE)
    win.blit(score_text, (5, (env.row + 1) * 35))

    pygame.display.flip()  # Update the display
    clock.tick(5)  # Game speed

pygame.quit()
