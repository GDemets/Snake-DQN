import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((450, 620))
clock = pygame.time.Clock()
running = True

item_pos_x = 225
item_pos_y = 0
alive = True
direction = None 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    snake = pygame.draw.circle(screen, (255,0,0), (item_pos_x, item_pos_y), 10)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and direction != "right":
        direction = "left"
    if keys[pygame.K_d] and direction != "left":
        direction = "right"
    if keys[pygame.K_w] and direction != "down":
        direction = "up"
    if keys[pygame.K_s] and direction != "up":
        direction = "down"

    if direction == "left":
        item_pos_x -= 1
    if direction == "right":
        item_pos_x += 1
    if direction == "up":
        item_pos_y -= 1
    if direction == "down":
        item_pos_y += 1

    if item_pos_x > 450:
        item_pos_x = 0
    if item_pos_x < 0:
        item_pos_x = 450
    if item_pos_y > 620:
        item_pos_y = 0
    if item_pos_y < 0:
        item_pos_y = 620

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
