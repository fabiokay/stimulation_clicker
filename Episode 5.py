# first try at a idle clicker game

# Pygame library import
import pygame
import pygame.mixer
import time

pygame.init()
pygame.mixer.init()

pygame.mixer_music.load("/Users/fabiokempf/PycharmProjects/Clicker/Audio/Focus.wav")
pygame.mixer.music.play(-1)

# display
screen = pygame.display.set_mode([300, 450])
pygame.display.set_caption("Adventure Capital")

# color library
black = pygame.Color("#222431")
grey  = pygame.Color("#a7b1c1")
violet = pygame.Color("#52489C")
petrol= pygame.Color("#4062BB")
blue = pygame.Color("#59C3C3")
white = pygame.Color("#EBEBEB")
pink = pygame.Color("#F45B69")

background = black
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 13)
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

# draw buttons functions
violet_cost = 1
violet_owned = False
violet_manager_cost = 100
petrol_cost = 2
petrol_owned = False
petrol_manager_cost = 500
blue_cost   = 3
blue_owned = False
blue_manager_cost = 1800
white_cost  = 4
white_owned = False
white_manager_cost = 5000
pink_cost   = 5
pink_owned = False
pink_manager_cost = 10000

# Kreis und Rechteck zeichnen
def draw_task(color, y_coord, value, draw, length, speed):
    global score
    if draw and length < 220:
        length += speed
    elif length >= 220:
        draw = False
        length = 0
        score += value
    task = pygame.draw.circle(screen, color, (30, y_coord), 20, 5)
    pygame.draw.rect(screen, color, [70, y_coord - 15, 220, 30])
    pygame.draw.rect(screen, black, [75, y_coord - 10, 210, 20])
    pygame.draw.rect(screen, color, [70, y_coord - 15, length, 30])
    value_text = font.render(str(round(value,2)), True, white)
    screen.blit(value_text, (16, y_coord - 7))
    return task, length, draw

# draw buttons
def draw_buttons(color, x_coord, cost, owned, manager_cost):
    color_button = pygame.draw.rect(screen, color, [x_coord, 340, 50, 30], 0, 6)
    color_cost = font.render(str(round(cost, 2)), True, black)
    screen.blit(color_cost, (x_coord + 2, 350))
    if not owned:
        manager_button = pygame.draw.rect(screen, color, [x_coord, 405, 50, 30], 0, 6)
        manager_text = font.render(str(round(manager_cost, 2)), True, black)
        screen.blit(manager_text, (x_coord + 2, 410))
    else: manager_button = pygame.draw.rect(screen, black, [x_coord, 405, 50, 30], 0, 6)

    return color_button, manager_button

running = True
while running:
    timer.tick(framerate)
    if violet_owned and not draw_violet:
        draw_violet = True
    if petrol_owned and not draw_petrol:
        draw_petrol = True
    if blue_owned and not draw_blue:
        draw_blue = True
    if white_owned and not draw_white:
        draw_white = True
    if pink_owned and not draw_pink:
        draw_pink = True
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
            #Managers buy - was passiert mit denen
            if violet_manager_buy.collidepoint(event.pos) and score >= violet_manager_cost and not violet_owned:
                violet_owned = True
                score -= violet_manager_cost
            if petrol_manager_buy.collidepoint(event.pos) and score >= petrol_manager_cost and not petrol_owned:
                petrol_owned = True
                score -= petrol_manager_cost
            if blue_manager_buy.collidepoint(event.pos) and score >= blue_manager_cost and not blue_owned:
                blue_owned = True
                score -= blue_manager_cost
            if white_manager_buy.collidepoint(event.pos) and score >= white_manager_cost and not white_owned:
                white_owned = True
                score -= violet_manager_cost
            if pink_manager_buy.collidepoint(event.pos) and score >= pink_manager_cost and not pink_owned:
                pink_owned = True
                score -= pink_manager_cost
            #buy more
            if violet_buy.collidepoint(event.pos) and score >= violet_cost:
                violet_value += .15
                score -= violet_cost
                violet_cost += .1
            if petrol_buy.collidepoint(event.pos) and score >= petrol_cost:
                petrol_value += .3
                score -= petrol_cost
                petrol_cost += .2
            if blue_buy.collidepoint(event.pos) and score >= blue_cost:
                blue_value += .45
                score -= blue_cost
                blue_cost += .3
            if white_buy.collidepoint(event.pos) and score >= white_cost:
                white_value += .6
                score -= white_cost
                white_cost += .4
            if pink_buy.collidepoint(event.pos) and score >= pink_cost:
                pink_value += .75
                score -= pink_cost
                pink_cost += .5

    screen.fill(background)

#Setting and drawing the bars
    task1, violet_length, draw_violet = draw_task(violet, 50, violet_value, draw_violet, violet_length, violet_speed)
    task2, petrol_length, draw_petrol = draw_task(petrol, 110, petrol_value, draw_petrol, petrol_length, petrol_speed)
    task3, blue_length, draw_blue = draw_task(blue, 170, blue_value, draw_blue, blue_length, blue_speed)
    task4, white_length, draw_white = draw_task(white, 230, white_value, draw_white, white_length, white_speed)
    task5, pink_length, draw_pink = draw_task(pink, 290, pink_value, draw_pink, pink_length, pink_speed)

#Sets the buy managers and buy more buttons
    violet_buy, violet_manager_buy = draw_buttons(violet, 10, violet_cost, violet_owned, violet_manager_cost)
    petrol_buy, petrol_manager_buy = draw_buttons(petrol, 70, petrol_cost, petrol_owned, petrol_manager_cost)
    blue_buy, blue_manager_buy = draw_buttons(blue, 130, blue_cost, blue_owned, blue_manager_cost)
    white_buy, white_manager_buy = draw_buttons(white, 190, white_cost, white_owned, white_manager_cost)
    pink_buy, pink_manager_buy = draw_buttons(pink, 250, pink_cost, pink_owned, pink_manager_cost)

#printing the overall money at the top of the screen
    display_score = font.render("Money: € "+str(round(score, 2)), True, grey, black)
    screen.blit(display_score, (10, 5))

#printing the buy more text
    buy_more = font.render("Buy more:", True, grey)
    screen.blit(buy_more, (10, 320))

#printing buy managers text
    buy_managers = font.render("Buy managers:", True, grey)
    screen.blit(buy_managers, (10, 385))

    pygame.display.flip()

pygame.quit()