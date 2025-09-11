# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((450, 620))
clock = pygame.time.Clock()
running = True

item_pos_x = 225
item_pos_y = 0



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))

    ############ RENDER YOUR GAME HERE ############
    pygame.draw.circle(screen, (255,0,0), (item_pos_x,item_pos_y), 10)
    item_pos_y += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        item_pos_x -= 1
    if keys[pygame.K_d]:
        item_pos_x += 1
    
    ###############################################
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()