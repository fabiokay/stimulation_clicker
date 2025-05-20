
#Pygame library import

import pygame
import pygame.mixer
import sys
import time
import math

pygame.init()
pygame.mixer.init()

pygame.mixer_music.load("/Users/fabiokempf/PycharmProjects/Clicker/Audio/Focus.wav")
pygame.mixer.music.play(-1)

# color library
black = pygame.Color("#222431")
grey  = pygame.Color("#a7b1c1")
violet = pygame.Color("#52489C")
petrol= pygame.Color("#4062BB")
blue = pygame.Color("#59C3C3")
white = pygame.Color("#EBEBEB")
pink = pygame.Color("#F45B69")

# --- display, timer,  and stuff ---
width = 720
height = 720
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
pygame.display.set_caption("StImUlAtIoN ClIcKeR")
running = True
background = black
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)

#game variables
score = 0
score_value = 1

# --- Flags
button_x2_visible = False
button_auto_visible = False
auto_clicker_active = False
button_buy_ball_visible = True
ball_bought = False


# --- Ball properties for the third layer
ball_radius = 15
ball_x, ball_y = width // 2, height // 2
ball_dx, ball_dy = 3, 4

# --- Trail history for the ball
trail = []
max_trail_length = 15

# --- Mitte Koordinaten
x_coord = width / 2
y_coord = height / 2

# --- Define a custom event for auto-clicking for auto clicker
AUTO_CLICK_EVENT = pygame.USEREVENT + 1
AUTO_CLICK_DELAY = 500  # 1000ms = 1 second

# --- Main Button drawing
main_button = pygame.draw.rect(screen, grey, [x_coord - 50, y_coord - 150, 100, 50], 0, 10)
main_button_text = font.render("Click me!", True, black)
screen.blit(main_button_text, (main_button.x + 25, main_button.y + 20))

button_x2 = pygame.draw.rect(screen, pink, [x_coord - 50, y_coord + 50, 100, 50], 0, 10)
button_x2_text = font.render("buy X2", True, black)
screen.blit(button_x2_text, (button_x2.x + 25, button_x2.y + 20))



running = True
while running:
    clock.tick(framerate) # limits FPS to 60

    if score >= 100 and not button_x2_visible:
        button_x2_visible = True

    if score >= 200 and not button_auto_visible:
        button_auto_visible = True

    # --- Events ---
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

            # --- Mausclickabfrage
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Main Button
            if main_button.collidepoint(event.pos):
                score += score_value
            # Auto Clicker
            if clicker_auto_button.collidepoint(event.pos):
                score -= 200
                pygame.time.set_timer(AUTO_CLICK_EVENT, AUTO_CLICK_DELAY)
                auto_clicker_active = True
                button_auto_visible = False
            # X2
            if button_x2.collidepoint(event.pos):
                score -= 100
                score_value += 1
                button_x2_visible = False



    # --- wenn true dann x2 sichtbar
    if button_x2_visible == True:
        button_x2 = pygame.draw.rect(screen, pink, [x_coord - 50, y_coord + 50, 100, 50], 0, 10)
        button_x2_text = font.render("buy X2", True, black)
        screen.blit(button_x2_text, (button_x2.x + 25, button_x2.y + 20))

    # --- wenn true
    if button_auto_visible == True:
        clicker_auto_button = pygame.draw.rect(screen, violet, [x_coord - 50, y_coord + 110, 100, 50], 0, 10)
        auto_clicker_text = font.render("buy auto", True, black)
        screen.blit(auto_clicker_text, (clicker_auto_button.x + 25, clicker_auto_button.y + 20))

    # --- Mausclickabfrage
        if event.type == pygame.MOUSEBUTTONDOWN:
        # Main Button
            if main_button.collidepoint(event.pos):
                score += score_value
        # Auto Clicker
            if auto_clicker.collidepoint(event.pos):
                score -= 200
                pygame.time.set_timer(AUTO_CLICK_EVENT, AUTO_CLICK_DELAY)
                auto_clicker_active = True
                button_auto_visible = False
        # X2
            if button_x2.collidepoint(event.pos):
                score -= 100
                score_value += 1
                button_x2_visible = False

    # --- wenn auto clicker gekauft, jede sekunde plus 1 score
    if event.type == AUTO_CLICK_EVENT and auto_clicker_active:
        score += 1  # Auto click adds 1 every second

# --- BALL ---
    # --- ball kaufen ---
    if score >= 300 and button_buy_ball_visible == True:
        button_buy_ball = pygame.draw.rect(screen, petrol, [x_coord - 50, y_coord + 170, 100, 50], 0, 10)
        button_ball_text = font.render("Buy a Ball!", True, black)
        screen.blit(button_ball_text, button_buy_ball)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_buy_ball.collidepoint(event.pos):
                score -= 300
                button_buy_ball_visible = False
                ball_bought = True

    # --- ball erscheint nach kauf ---
    if ball_bought == True:
        # --- Draw Ball ---
        pygame.draw.circle(screen, petrol, (ball_x, ball_y), ball_radius)

        # --- update ball position ---
        ball_x += ball_dx
        ball_y += ball_dy

        # --- Add current position to trail
        trail.append((ball_x, ball_y))
        if len(trail) > max_trail_length:
            trail.pop(0)

        # --- Bounce off edges
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
            ball_dx *= -1
            score += 10
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
            ball_dy *= -1
            score += 10

        # --- Draw Trail ---
        for i, (tx, ty) in enumerate(trail):
            fade = int(255 * (i + 1) / max_trail_length)
            trail_color = (37, 150, 190, fade)
            # Create a small surface with alpha channel
            trail_surf = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, trail_color, (ball_radius, ball_radius), ball_radius)
            screen.blit(trail_surf, (tx - ball_radius, ty - ball_radius))



    # --- Show score
    score_text = font.render("Energy: " + str(score), True, grey)
    screen.blit(score_text, (x_coord, 10))
    
    pygame.display.flip()

pygame.quit()