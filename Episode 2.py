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
draw_violet = False
draw_petrol = False
draw_blue = False
draw_white = False
draw_pink = False
violet_length = 0
petrol_length = 0
blue_length = 0
white_length = 0
pink_length = 0
violet_speed = 5
petrol_speed = 4
blue_speed = 3
white_speed = 2
pink_speed = 1
score = 0



#Kreis und Rechteck zeichnen
def draw_task(color, y_coord, value, draw, length, speed):
    global score
    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        score += value
    task = pygame.draw.circle(screen, color, (30, y_coord), 20, 5)
    pygame.draw.rect(screen, color, [70, y_coord - 15, 200, 30])
    pygame.draw.rect(screen, black, [75, y_coord - 10, 190, 20])
    pygame.draw.rect(screen, color, [70, y_coord - 15, length, 30])
    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_coord - 10))
    return task, length, draw

running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if task1.collidepoint(event.pos):
                draw_violet = True
            if task2.collidepoint(event.pos):
                draw_petrol = True
            if task3.collidepoint(event.pos):
                draw_blue = True
            if task4.collidepoint(event.pos):
                draw_white = True
            if task5.collidepoint(event.pos):
                draw_pink = True

    screen.fill(background)
    task1, violet_length, draw_violet = draw_task(violet, 50, violet_value, draw_violet, violet_length, violet_speed)
    task2, petrol_length, draw_petrol = draw_task(petrol, 110, petrol_value, draw_petrol, petrol_length, petrol_speed)
    task3, blue_length, draw_blue = draw_task(blue, 170, blue_value, draw_blue, blue_length, blue_speed)
    task4, white_length, draw_white = draw_task(white, 230, white_value, draw_white, white_length, white_speed)
    task5, pink_length, draw_pink = draw_task(pink, 290, pink_value, draw_pink, pink_length, pink_speed)

    display_score = font.render("Money: € "+str(round(score, 2)), True, grey, black)
    screen.blit(display_score, (10, 5))
    pygame.display.flip()
pygame.quit()