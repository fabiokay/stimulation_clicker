import pygame
import pygame.mixer
import sys
import random # For critical clicks

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("/Audio/Focus.wav")
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
CRITICAL_CHANCE = 0.05  # 5% chance
CRITICAL_MULTIPLIER = 5 # 5x score on critical
critical_feedback_text = ""
critical_feedback_timer = 0
CRITICAL_FEEDBACK_DURATION = 60 # Frames (e.g., 1 second at 60 FPS)
critical_chance_upgrade_cost = 1000
critical_multiplier_upgrade_cost = 1500


# --- Flags ---
button_x2_visible = False
button_plus_five_click_visible = False
button_plus_ten_click_visible = False
button_auto_visible = False
auto_clicker_active = False
button_buy_ball_visible = False
ball_bought = False
plus_ten_ball_upgrade_unlocked = False # Flag for the +10 ball bounce upgrade
button_crit_chance_upgrade_visible = False
button_crit_multiplier_upgrade_visible = False

# --- Particle System ---
particles = []
MAX_PARTICLES = 150 # Adjust for performance/density
PARTICLE_SPAWN_RATE = 2 # Particles to spawn per frame (if under MAX_PARTICLES)

class Particle:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.size = random.randint(1, 3)
        # Slightly brighter colors for better visibility
        r = random.randint(60, 120)
        g = random.randint(30, 160)
        b = random.randint(40, 180)
        self.color_base = (r, g, b)
        self.dx = random.uniform(-0.3, 0.3)
        self.dy = random.uniform(-0.2, 0.2) # Slightly slower vertical drift
        self.lifetime = random.randint(120, 300) # 2 to 5 seconds at 60 FPS
        self.initial_lifetime = float(self.lifetime) # Store as float for division

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(200 * (self.lifetime / self.initial_lifetime)) # Max alpha 200 for subtlety
            alpha = max(0, min(200, alpha))
            
            # Create a temporary surface for alpha blending if not using per-pixel alpha directly
            # For simple circles, drawing directly with an RGBA color is often fine if supported
            # pygame.draw.circle(surface, self.color_base + (alpha,), (int(self.x), int(self.y)), self.size)
            # Using a surface for potentially better alpha control or more complex shapes later
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, self.color_base + (alpha,), (self.size, self.size), self.size)
            surface.blit(particle_surf, (self.x - self.size, self.y - self.size))

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

    # --- Particle System Update and Draw ---
    # Spawn new particles
    if len(particles) < MAX_PARTICLES:
        for _ in range(PARTICLE_SPAWN_RATE):
            if len(particles) < MAX_PARTICLES: # Check again in case loop fills it
                particles.append(Particle(width, height))

    # Update and draw particles
    active_particles = []
    for p in particles:
        p.update()
        if p.lifetime > 0:
            p.draw(screen)
            active_particles.append(p)
    particles = active_particles

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
    if score >= 800: # Unlock condition for critical chance upgrade
        button_crit_chance_upgrade_visible = True
    if score >= 1200: # Unlock condition for critical multiplier upgrade
        button_crit_multiplier_upgrade_visible = True

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

    # --- Draw Critical Upgrade Buttons ---
    crit_upgrade_y = button_y_start + button_spacing_y * 4 # New row for critical upgrades
    button_crit_chance_upgrade = None
    button_crit_multiplier_upgrade = None

    if button_crit_chance_upgrade_visible:
        button_crit_chance_upgrade = pygame.draw.rect(screen, pink, [button_col1_x, crit_upgrade_y, 100, 50], 0, 10)
        crit_chance_text = font.render("Crit Chance+", True, black)
        screen.blit(crit_chance_text, (button_crit_chance_upgrade.x + 5, button_crit_chance_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_chance_upgrade_cost)}", True, white), (button_crit_chance_upgrade.right + 10, button_crit_chance_upgrade.y + 17))
        screen.blit(font.render(f"({CRITICAL_CHANCE*100:.0f}%)", True, white), (button_crit_chance_upgrade.x + 20, button_crit_chance_upgrade.y - 15))


    if button_crit_multiplier_upgrade_visible:
        button_crit_multiplier_upgrade = pygame.draw.rect(screen, pink, [button_col2_x, crit_upgrade_y, 100, 50], 0, 10)
        crit_multi_text = font.render("Crit Multi+", True, black)
        screen.blit(crit_multi_text, (button_crit_multiplier_upgrade.x + 5, button_crit_multiplier_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_multiplier_upgrade_cost)}", True, white), (button_crit_multiplier_upgrade.right + 10, button_crit_multiplier_upgrade.y + 17))
        screen.blit(font.render(f"(x{CRITICAL_MULTIPLIER:.1f})", True, white), (button_crit_multiplier_upgrade.x + 25, button_crit_multiplier_upgrade.y - 15))

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

            if button_crit_chance_upgrade and button_crit_chance_upgrade.collidepoint(event.pos) and score >= critical_chance_upgrade_cost:
                score -= critical_chance_upgrade_cost
                CRITICAL_CHANCE = min(CRITICAL_CHANCE + 0.01, 0.5) # Increase by 1%, cap at 50%
                critical_chance_upgrade_cost *= 1.9

            if button_crit_multiplier_upgrade and button_crit_multiplier_upgrade.collidepoint(event.pos) and score >= critical_multiplier_upgrade_cost:
                score -= critical_multiplier_upgrade_cost
                CRITICAL_MULTIPLIER += 0.5 # Increase by 0.5
                critical_multiplier_upgrade_cost *= 2.0




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
