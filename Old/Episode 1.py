# first try at a idle clicker game

import pygame
pygame.init()

#display
screen = pygame.display.set_mode([300, 450])
pygame.display.set_caption("Adventure Capital")

#color library
black = pygame.Color("#222431")
grey  = pygame.Color("#a7b1c1")
violet = pygame.Color("#52489C")
petrol= pygame.Color("#4062BB")
blue = pygame.Color("#59C3C3")
white = pygame.Color("#EBEBEB")
pink = pygame.Color("#F45B69")

background = black
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

# game variables
violet_value = 1
petrol_value = 2
blue_value   = 3
white_value  = 4
pink_value   = 5


#Kreis und Rechteck zeichnen
def draw_task(color, y_coord, value):
    pygame.draw.circle(screen, color, (30, y_coord), 20, 5)
    pygame.draw.rect(screen, color, [70, y_coord - 15, 200, 30])
    pygame.draw.rect(screen, black, [75, y_coord - 10, 190, 20])
    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_coord - 10))

running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)
    draw_task(violet, 50, violet_value)
    draw_task(petrol, 110, petrol_value)
    draw_task(blue, 170, blue_value)
    draw_task(white, 230, white_value)
    draw_task(pink, 290, pink_value)
    pygame.display.flip()
pygame.quit()