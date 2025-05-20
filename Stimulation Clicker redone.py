import pygame
import pygame.mixer
import sys
import random # For critical clicks

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("/Users/fabiokempf/PycharmProjects/Clicker/Audio/Focus.wav")
pygame.mixer.music.play(-1)

# --- Colors ---
black = pygame.Color("#222431")
grey  = pygame.Color("#a7b1c1")
violet = pygame.Color("#52489C")
petrol = pygame.Color("#4062BB")
blue = pygame.Color("#59C3C3")
white = pygame.Color("#EBEBEB")
pink = pygame.Color("#F45B69")

# --- Display Setup ---
width, height = 720, 720
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
pygame.display.set_caption("StImUlAtIoN ClIcKeR")
font = pygame.font.Font("freesansbold.ttf", 16)
framerate = 60

# --- Game Variables ---
#global score
score = 0
score_value = 1
x2_cost = 100 # Cost for "+1" click upgrade
plus_five_click_cost = 500 # Cost for "+5" click upgrade
plus_ten_click_cost = 2000 # Cost for "+10" click upgrade
bounce = 10
plus_ten_ball_cost = 400 # Cost for "+10" ball bounce upgrade
auto_clicker_cost = 200
auto_click_power = 1 # Amount per auto-click
auto_power_upgrade_cost = 300
auto_speed_upgrade_cost = 400
running = True

# --- Critical Click Variables ---
CRITICAL_CHANCE = 0.10  # 10% chance
CRITICAL_MULTIPLIER = 5 # 5x score on critical
critical_feedback_text = ""
critical_feedback_timer = 0
CRITICAL_FEEDBACK_DURATION = 60 # Frames (e.g., 1 second at 60 FPS)


# --- Flags ---
button_x2_visible = False
button_plus_five_click_visible = False
button_plus_ten_click_visible = False
button_auto_visible = False
auto_clicker_active = False
button_buy_ball_visible = False
ball_bought = False
plus_ten_ball_upgrade_unlocked = False # Flag for the +10 ball bounce upgrade

# --- Ball Properties ---
ball_radius = 15
ball_x, ball_y = width // 2, height // 2
ball_dx, ball_dy = 3, 4
trail = []
max_trail_length = 15

# --- Coordinates ---
x_coord, y_coord = width / 2, height / 2

# --- Events ---
AUTO_CLICK_EVENT = pygame.USEREVENT + 1
INITIAL_AUTO_CLICK_DELAY = 500
current_auto_click_delay = INITIAL_AUTO_CLICK_DELAY

# --- Game Loop ---
while running:
    clock.tick(framerate)
    screen.fill(black)

    # --- Check Unlocks ---
    if score >= 100:
        button_x2_visible = True
    if score >= 400: # Unlock condition for "+5" click
        button_plus_five_click_visible = True
    if score >= 1500: # Unlock condition for "+10" click
        button_plus_ten_click_visible = True
    if score >= 200:
        button_auto_visible = True
    if score >= 300:
        button_buy_ball_visible = True
    if ball_bought and score >= plus_ten_ball_cost: # Unlock condition for the +10 ball bounce upgrade
        plus_ten_ball_upgrade_unlocked = True

    # --- Draw Main Button ---
    main_button = pygame.draw.rect(screen, grey, [x_coord - 50, y_coord - 150, 100, 50], 0, 10)
    main_button_text = font.render("Click me!", True, black)
    screen.blit(main_button_text, (main_button.x + 10, main_button.y + 15))

    # --- Define button layout positions ---
    button_y_start = y_coord - 50 # Start Y for the first row of upgrade buttons
    button_col1_x = x_coord - 160 # X for the left column of buttons
    button_col2_x = x_coord + 60  # X for the right column of buttons
    button_spacing_y = 60 # Vertical spacing between buttons

    # --- Column 1: Click Upgrades ---

    # --- Draw "+1" Click Button (formerly X2) ---
    if button_x2_visible:
        button_x2 = pygame.draw.rect(screen, pink, [button_col1_x, button_y_start, 100, 50], 0, 10)
        button_x2_text = font.render("buy +1", True, black)
        screen.blit(button_x2_text, (button_x2.x + 10, button_x2.y + 15))
        screen.blit(font.render("Cost: " + str(round(x2_cost)), True, white), (button_x2.right + 10, button_x2.y + 17))
    else:
        button_x2 = None

    # --- Draw "+5" Click Button ---
    if button_plus_five_click_visible:
        button_plus_five_click = pygame.draw.rect(screen, blue, [button_col1_x, button_y_start + button_spacing_y, 100, 50], 0, 10)
        plus_five_text = font.render("buy +5", True, black)
        screen.blit(plus_five_text, (button_plus_five_click.x + 10, button_plus_five_click.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_five_click_cost)), True, white), (button_plus_five_click.right + 10, button_plus_five_click.y + 17))
    else:
        button_plus_five_click = None

    # --- Draw "+10" Click Button ---
    if button_plus_ten_click_visible:
        button_plus_ten_click = pygame.draw.rect(screen, white, [button_col1_x, button_y_start + button_spacing_y * 2, 100, 50], 0, 10)
        plus_ten_text = font.render("buy +10", True, black)
        screen.blit(plus_ten_text, (button_plus_ten_click.x + 5, button_plus_ten_click.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_ten_click_cost)), True, white), (button_plus_ten_click.right + 10, button_plus_ten_click.y + 17))
    else:
        button_plus_ten_click = None

    # --- Column 2: Other Upgrades ---

    # --- Draw Auto Clicker Button ---
    if button_auto_visible and not auto_clicker_active:
        clicker_auto_button = pygame.draw.rect(screen, violet, [button_col2_x, button_y_start, 100, 50], 0, 10)
        auto_clicker_text = font.render("buy auto", True, black)
        screen.blit(auto_clicker_text, (clicker_auto_button.x + 10, clicker_auto_button.y + 15))
        screen.blit(font.render("Cost: " + str(auto_clicker_cost), True, white), (clicker_auto_button.right + 10, clicker_auto_button.y + 17))
    else:
        clicker_auto_button = None  # to avoid reference errors

    # --- Draw Ball Purchase Button ---
    if button_buy_ball_visible and not ball_bought:
        button_buy_ball = pygame.draw.rect(screen, petrol, [button_col2_x, button_y_start + button_spacing_y, 100, 50], 0, 10)
        button_ball_text = font.render("Buy a Ball!", True, black)
        screen.blit(button_ball_text, (button_buy_ball.x + 5, button_buy_ball.y + 15))
        screen.blit(font.render("Cost: 300", True, white), (button_buy_ball.right + 10, button_buy_ball.y + 17))
    else:
        button_buy_ball = None

    # --- Draw "+10 Ball Bounce Value" Button ---
    if ball_bought and plus_ten_ball_upgrade_unlocked:
        button_plusten_ball = pygame.draw.rect(screen, white, [button_col2_x, button_y_start + button_spacing_y * 2, 100, 50], 0, 10)
        button_plusten_text = font.render("+10 Ball!", True, black) # Adjusted text slightly for space
        screen.blit(button_plusten_text, (button_plusten_ball.x + 5, button_plusten_ball.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_ten_ball_cost)), True, white), (button_plusten_ball.right + 10, button_plusten_ball.y + 17))
    else:
        button_plusten_ball = None

    # --- Draw Auto-Clicker Upgrade Buttons (if auto-clicker is active) ---
    button_auto_power_upgrade = None
    button_auto_speed_upgrade = None
    if auto_clicker_active:
        auto_upgrade_y = button_y_start + button_spacing_y * 3 # New row for these buttons

        # Auto Power Upgrade Button
        button_auto_power_upgrade = pygame.draw.rect(screen, violet, [button_col1_x, auto_upgrade_y, 100, 50], 0, 10)
        auto_power_text = font.render("Auto Pwr", True, black)
        screen.blit(auto_power_text, (button_auto_power_upgrade.x + 5, button_auto_power_upgrade.y + 15))
        screen.blit(font.render("Cost: " + str(round(auto_power_upgrade_cost)), True, white), (button_auto_power_upgrade.right + 10, button_auto_power_upgrade.y + 17))

        # Auto Speed Upgrade Button
        button_auto_speed_upgrade = pygame.draw.rect(screen, violet, [button_col2_x, auto_upgrade_y, 100, 50], 0, 10)
        auto_speed_text = font.render("Auto Spd", True, black)
        screen.blit(auto_speed_text, (button_auto_speed_upgrade.x + 5, button_auto_speed_upgrade.y + 15))
        screen.blit(font.render("Cost: " + str(round(auto_speed_upgrade_cost)), True, white), (button_auto_speed_upgrade.right + 10, button_auto_speed_upgrade.y + 17))

    # --- Draw Critical Feedback ---
    if critical_feedback_timer > 0:
        crit_text_surface = font.render(critical_feedback_text, True, pink) # Or another vibrant color
        # Position the text above the main click button
        text_rect = crit_text_surface.get_rect(center=(main_button.centerx, main_button.top - 20))
        screen.blit(crit_text_surface, text_rect)
        critical_feedback_timer -= 1
        if critical_feedback_timer <= 0:
            critical_feedback_text = "" # Clear text when timer is done

    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if main_button.collidepoint(event.pos):
                if random.random() < CRITICAL_CHANCE:
                    # Critical Hit!
                    crit_amount = score_value * CRITICAL_MULTIPLIER
                    score += crit_amount
                    critical_feedback_text = f"CRITICAL! +{crit_amount}"
                    critical_feedback_timer = CRITICAL_FEEDBACK_DURATION
                else:
                    # Normal Click
                    score += score_value


            if button_x2 and button_x2.collidepoint(event.pos) and score >= x2_cost:
                score -= x2_cost
                score_value += 1
                x2_cost *= 1.5

            if button_plus_five_click and button_plus_five_click.collidepoint(event.pos) and score >= plus_five_click_cost:
                score -= plus_five_click_cost
                score_value += 5
                plus_five_click_cost *= 1.6

            if button_plus_ten_click and button_plus_ten_click.collidepoint(event.pos) and score >= plus_ten_click_cost:
                score -= plus_ten_click_cost
                score_value += 10
                plus_ten_click_cost *= 1.8

            if clicker_auto_button and clicker_auto_button.collidepoint(event.pos) and score >= auto_clicker_cost:
                score -= auto_clicker_cost
                pygame.time.set_timer(AUTO_CLICK_EVENT, current_auto_click_delay)
                auto_clicker_active = True
                button_auto_visible = False

            if button_buy_ball and button_buy_ball.collidepoint(event.pos) and score >= 300:
                score -= 300
                button_buy_ball_visible = False
                ball_bought = True

            if button_plusten_ball and button_plusten_ball.collidepoint(event.pos) and score >= plus_ten_ball_cost:
                score -= plus_ten_ball_cost
                bounce += 10
                plus_ten_ball_cost *= 1.7 # Increase cost for next purchase
            
            if button_auto_power_upgrade and button_auto_power_upgrade.collidepoint(event.pos) and score >= auto_power_upgrade_cost:
                score -= auto_power_upgrade_cost
                auto_click_power += 1 # Or some other increment like * 1.5
                auto_power_upgrade_cost *= 1.7

            if button_auto_speed_upgrade and button_auto_speed_upgrade.collidepoint(event.pos) and score >= auto_speed_upgrade_cost:
                score -= auto_speed_upgrade_cost
                current_auto_click_delay = max(50, current_auto_click_delay - 50) # Decrease delay, min 50ms
                auto_speed_upgrade_cost *= 1.8
                pygame.time.set_timer(AUTO_CLICK_EVENT, current_auto_click_delay) # Re-set timer with new speed


        elif event.type == AUTO_CLICK_EVENT and auto_clicker_active:
            score += auto_click_power

    # --- Ball Drawing and Movement ---
    if ball_bought:
        ball_x += ball_dx
        ball_y += ball_dy
        trail.append((ball_x, ball_y))
        if len(trail) > max_trail_length:
            trail.pop(0)

        # Bounce and score
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
            ball_dx *= -1
            score += bounce
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
            ball_dy *= -1
            score += bounce

        # Draw trail
        for i, (tx, ty) in enumerate(trail):
            fade = int(255 * (i + 1) / max_trail_length)
            trail_color = (37, 150, 190, fade)
            trail_surf = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, trail_color, (ball_radius, ball_radius), ball_radius)
            screen.blit(trail_surf, (tx - ball_radius, ty - ball_radius))

        # Draw Ball
        pygame.draw.circle(screen, petrol, (ball_x, ball_y), ball_radius)

    # --- Show Score ---
    score_text = font.render("Energy: " + str(round(score,0)), True, grey)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
