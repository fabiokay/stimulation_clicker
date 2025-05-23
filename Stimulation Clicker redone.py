import pygame
import pygame.mixer
import sys # Not used but good practice
import random # For critical clicks
import Colors # Importing the colors from the Colors.py file

pygame.init()
pygame.mixer.init()

# --- Audio Setup ---
pygame.mixer.pre_init(44100, -16, 2, 2048) # Pre-initialize mixer for better performance
pygame.mixer.set_num_channels(8) # Set number of channels for sound effects
# Load sound effects
click_sounds = [
    pygame.mixer.Sound("Audio/Click_1.wav"),
    pygame.mixer.Sound("Audio/Click_2.wav"),
    pygame.mixer.Sound("Audio/Click_3.wav"),
    pygame.mixer.Sound("Audio/Click_4.wav"),
    pygame.mixer.Sound("Audio/Click_5.wav"),
]
sound_upgrade = pygame.mixer.Sound("Audio/Upgrade.wav")
sound_unlock = pygame.mixer.Sound("Audio/Unlock.wav")
sound_supernova = pygame.mixer.Sound("Audio/Supernova.wav")
# Load background music
pygame.mixer.music.load("Audio/Focus.wav")
pygame.mixer.music.play(-1)

# --- Colors ---
#black = pygame.Color("#222431")
#grey  = pygame.Color("#a7b1c1") 
#violet = pygame.Color("#52489C")
#petrol = pygame.Color("#4062BB")
#blue = pygame.Color("#59C3C3")
#white = pygame.Color("#EBEBEB")
#pink = pygame.Color("#F45B69")

# --- Display Setup ---
width, height = 1280, 720
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
pygame.display.set_caption("StImUlAtIoN ClIcKeR")
font = pygame.font.Font("freesansbold.ttf", 16)
framerate = 60

# --- Game Variables ---
#global score
score = 0
click_count = 0 # To count total clicks on the main button
score_value = 1
x2_cost = 100 # Cost for "+1" click upgrade
plus_five_click_cost = 500 # Cost for "+5" click upgrade
plus_ten_click_cost = 2000 # Cost for "+10" click upgrade
bounce = 10 # Bounce value for the ball
plus_ten_ball_cost = 400 # Cost for "+10" ball bounce upgrade
auto_clicker_cost = 200 # Cost for auto-clicker

# --- Auto Clicker Variables ---
auto_click_power = 1 # Amount per auto-click
auto_power_upgrade_cost = 300
auto_speed_upgrade_cost = 400
running = True

# --- Critical Click Variables ---
CRITICAL_CHANCE = 0.05  # 5% chance
CRITICAL_MULTIPLIER = 5 # 5x score on critical
critical_feedback_text = ""
critical_feedback_timer = 0
CRITICAL_FEEDBACK_DURATION = 10 # Frames (e.g., 1 second at 60 FPS)
critical_chance_upgrade_cost = 1000
critical_multiplier_upgrade_cost = 1500
critical_hit_unlock_cost = 750 # Cost to unlock critical hits

# --- Supernova Variables ---
SUPERNOVA_DURATION_MS = 10000  # 10 seconds
SUPERNOVA_COOLDOWN_MS = 120000  # 120 seconds
SUPERNOVA_CLICK_MULTIPLIER = 20
supernova_unlock_score = 10000 # Score needed to see the Supernova button
supernova_active = False
supernova_start_time = 0
supernova_cooldown_start_time = 0
supernova_ready = True # True if not active and not on cooldown
button_supernova_visible = False

# --- EPS (Energy Per Second) Variables ---
current_eps = 0.0
gross_energy_earned_in_interval = 0.0 # Accumulates energy earned for EPS calculation
last_eps_calc_time = 0      # Will be initialized with pygame.time.get_ticks()
eps_calculation_interval = 1000 # milliseconds (e.g., 1 second)

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
critical_hit_unlocked = False # Player starts without critical hits
button_critical_hit_unlock_visible = False

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
    if score >= 500 and not critical_hit_unlocked: # Unlock condition for critical hit unlock
        button_critical_hit_unlock_visible = True
    if critical_hit_unlocked and score >= critical_chance_upgrade_cost: # Unlock condition for critical chance upgrade
        button_crit_chance_upgrade_visible = True
    if critical_hit_unlocked and score >= critical_multiplier_upgrade_cost: # Unlock condition for critical multiplier upgrade
        button_crit_multiplier_upgrade_visible = True
    if score >= supernova_unlock_score and not button_supernova_visible and not supernova_active : # Unlock condition for Supernova
        button_supernova_visible = True

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
    button_critical_hit_unlock = None

    # --- Draw Critical Hit Unlock Button ---
    if button_critical_hit_unlock_visible and not critical_hit_unlocked:
        button_critical_hit_unlock = pygame.draw.rect(screen, pink, [button_col1_x, crit_upgrade_y, 100, 50], 0, 10)
        unlock_crit_text = font.render("Unlock Crits", True, black)
        screen.blit(unlock_crit_text, (button_critical_hit_unlock.x + 5, button_critical_hit_unlock.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_hit_unlock_cost)}", True, white), (button_critical_hit_unlock.right + 10, button_critical_hit_unlock.y + 17))


    if critical_hit_unlocked and button_crit_chance_upgrade_visible:
        # Adjust Y position if unlock button was previously there or manage layout differently
        crit_chance_y_pos = crit_upgrade_y if not button_critical_hit_unlock_visible else crit_upgrade_y # Or shift down: crit_upgrade_y + button_spacing_y
        button_crit_chance_upgrade = pygame.draw.rect(screen, pink, [button_col1_x, crit_chance_y_pos, 100, 50], 0, 10)
        crit_chance_text = font.render("Crit Chance+", True, black)
        screen.blit(crit_chance_text, (button_crit_chance_upgrade.x + 5, button_crit_chance_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_chance_upgrade_cost)}", True, white), (button_crit_chance_upgrade.right + 10, button_crit_chance_upgrade.y + 17))
        screen.blit(font.render(f"({CRITICAL_CHANCE*100:.0f}%)", True, white), (button_crit_chance_upgrade.x + 20, button_crit_chance_upgrade.y - 15))


    if critical_hit_unlocked and button_crit_multiplier_upgrade_visible:
        crit_multi_y_pos = crit_upgrade_y # Or shift down if needed
        button_crit_multiplier_upgrade = pygame.draw.rect(screen, pink, [button_col2_x, crit_multi_y_pos, 100, 50], 0, 10)
        crit_multi_text = font.render("Crit Multi+", True, black)
        screen.blit(crit_multi_text, (button_crit_multiplier_upgrade.x + 5, button_crit_multiplier_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_multiplier_upgrade_cost)}", True, white), (button_crit_multiplier_upgrade.right + 10, button_crit_multiplier_upgrade.y + 17))
        screen.blit(font.render(f"(x{CRITICAL_MULTIPLIER:.1f})", True, white), (button_crit_multiplier_upgrade.x + 25, button_crit_multiplier_upgrade.y - 15))

    # --- Draw Supernova Button ---
    button_supernova = None
    # Place Supernova button in a new row, or adjust existing layout if preferred
    supernova_button_y = button_y_start + button_spacing_y * 5 
    if button_supernova_visible:
        button_color = grey # Default
        supernova_text_str = "Supernova"
        current_time_ticks_draw = pygame.time.get_ticks()

        if supernova_active:
            button_color = pink # Active color
            remaining_time_s = max(0, (SUPERNOVA_DURATION_MS - (current_time_ticks_draw - supernova_start_time)) // 1000)
            supernova_text_str = f"Active: {remaining_time_s}s"
        elif not supernova_ready: # On cooldown
            button_color = violet # Cooldown color
            remaining_cooldown_s = max(0, (SUPERNOVA_COOLDOWN_MS - (current_time_ticks_draw - supernova_cooldown_start_time)) // 1000)
            supernova_text_str = f"CD: {remaining_cooldown_s}s"
        else: # Ready
            button_color = blue # Ready color
            supernova_text_str = "Supernova!"
        
        button_supernova = pygame.draw.rect(screen, button_color, [button_col1_x, supernova_button_y, 100, 50], 0, 10) # Standard button size
        supernova_text_render = font.render(supernova_text_str, True, black if supernova_active or supernova_ready else white) # Text color contrast
        text_rect_supernova = supernova_text_render.get_rect(center=button_supernova.center)
        screen.blit(supernova_text_render, text_rect_supernova)

    # --- Draw Critical Feedback ---
    if critical_feedback_timer > 0:
        crit_text_surface = font.render(critical_feedback_text, True, pink) # Or another vibrant color
        # Position the text above the main click button
        text_rect = crit_text_surface.get_rect(center=(main_button.centerx, main_button.top - 20))
        screen.blit(crit_text_surface, text_rect)
        critical_feedback_timer -= 1
        if critical_feedback_timer <= 0:
            critical_feedback_text = "" # Clear text when timer is done

    # --- Supernova State Management ---
    current_time_ticks_logic = pygame.time.get_ticks()
    if supernova_active:
        if current_time_ticks_logic - supernova_start_time >= SUPERNOVA_DURATION_MS:
            supernova_active = False
            # Cooldown already started when activated, so no need to set supernova_cooldown_start_time here again.
            # The button will become visible again if score is still high enough.
    elif not supernova_ready: # If not active, check if cooldown is over
        if current_time_ticks_logic - supernova_cooldown_start_time >= SUPERNOVA_COOLDOWN_MS:
            supernova_ready = True

    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if main_button.collidepoint(event.pos):
                base_click_value_for_this_click = score_value
                if supernova_active:
                    base_click_value_for_this_click *= SUPERNOVA_CLICK_MULTIPLIER

                if critical_hit_unlocked: # Only check for crits if unlocked
                    if random.random() < CRITICAL_CHANCE:
                        # Critical Hit!
                        # Crit multiplier applies to the (potentially Supernova-boosted) base gain
                        crit_amount = base_click_value_for_this_click * CRITICAL_MULTIPLIER
                        score += crit_amount
                        gross_energy_earned_in_interval += crit_amount
                        critical_feedback_text = f"CRITICAL! +{crit_amount}"
                        critical_feedback_timer = CRITICAL_FEEDBACK_DURATION
                    else:
                        # Normal Click (Supernova-boosted if active)
                        score += base_click_value_for_this_click
                        gross_energy_earned_in_interval += base_click_value_for_this_click
                else: # If crits not unlocked, always a normal click
                    score += base_click_value_for_this_click # (Supernova-boosted if active)
                    gross_energy_earned_in_interval += base_click_value_for_this_click
                click_count += 1 # Increment click counter
                random.choice(click_sounds).play() # Play a randomly chosen click sound
                

            if button_x2 and button_x2.collidepoint(event.pos) and score >= x2_cost:
                score -= x2_cost
                score_value += 1
                x2_cost *= 1.5
                sound_upgrade.play()

            if button_plus_five_click and button_plus_five_click.collidepoint(event.pos) and score >= plus_five_click_cost:
                score -= plus_five_click_cost
                score_value += 5
                plus_five_click_cost *= 1.6
                sound_upgrade.play()

            if button_plus_ten_click and button_plus_ten_click.collidepoint(event.pos) and score >= plus_ten_click_cost:
                score -= plus_ten_click_cost
                score_value += 10
                plus_ten_click_cost *= 1.8
                sound_upgrade.play()

            if clicker_auto_button and clicker_auto_button.collidepoint(event.pos) and score >= auto_clicker_cost:
                score -= auto_clicker_cost
                pygame.time.set_timer(AUTO_CLICK_EVENT, current_auto_click_delay)
                auto_clicker_active = True
                # This is an unlock, so it already plays sound_unlock
                sound_unlock.play() # Play unlock sound
                button_auto_visible = False

            if button_buy_ball and button_buy_ball.collidepoint(event.pos) and score >= 300:
                score -= 300
                button_buy_ball_visible = False
                ball_bought = True
                sound_unlock.play() # Play unlock sound

            if button_plusten_ball and button_plusten_ball.collidepoint(event.pos) and score >= plus_ten_ball_cost:
                score -= plus_ten_ball_cost
                bounce += 10
                plus_ten_ball_cost *= 1.7 # Increase cost for next purchase
                sound_upgrade.play() # This is an upgrade to an existing feature
            
            if button_auto_power_upgrade and button_auto_power_upgrade.collidepoint(event.pos) and score >= auto_power_upgrade_cost:
                score -= auto_power_upgrade_cost
                auto_click_power += 1
                auto_power_upgrade_cost *= 1.7
                sound_upgrade.play()

            if button_auto_speed_upgrade and button_auto_speed_upgrade.collidepoint(event.pos) and score >= auto_speed_upgrade_cost:
                score -= auto_speed_upgrade_cost
                current_auto_click_delay = max(50, current_auto_click_delay - 50) # Decrease delay, min 50ms
                auto_speed_upgrade_cost *= 1.8
                pygame.time.set_timer(AUTO_CLICK_EVENT, current_auto_click_delay) # Re-set timer with new speed
                sound_upgrade.play()
            
            if button_critical_hit_unlock and button_critical_hit_unlock.collidepoint(event.pos) and score >= critical_hit_unlock_cost:
                score -= critical_hit_unlock_cost
                critical_hit_unlocked = True
                # This is an unlock, so it already plays sound_unlock
                sound_unlock.play() # Play unlock sound
                button_critical_hit_unlock_visible = False # Hide the unlock button

            if button_crit_chance_upgrade and button_crit_chance_upgrade.collidepoint(event.pos) and score >= critical_chance_upgrade_cost:
                score -= critical_chance_upgrade_cost
                CRITICAL_CHANCE = min(CRITICAL_CHANCE + 0.01, 0.5) # Increase by 1%, cap at 50%
                critical_chance_upgrade_cost *= 1.9
                sound_upgrade.play()

            if button_crit_multiplier_upgrade and button_crit_multiplier_upgrade.collidepoint(event.pos) and score >= critical_multiplier_upgrade_cost:
                score -= critical_multiplier_upgrade_cost
                CRITICAL_MULTIPLIER += 0.5 # Increase by 0.5
                critical_multiplier_upgrade_cost *= 2.0
                sound_upgrade.play()
            
            if button_supernova and button_supernova.collidepoint(event.pos) and supernova_ready:
                supernova_active = True
                supernova_ready = False # It's now active, so not "ready" for another click until cooldown
                supernova_start_time = pygame.time.get_ticks()
                supernova_cooldown_start_time = pygame.time.get_ticks() # Cooldown timer starts immediately upon activation
                sound_supernova.play()


        elif event.type == AUTO_CLICK_EVENT and auto_clicker_active:
            score += auto_click_power
            gross_energy_earned_in_interval += auto_click_power

    # --- EPS Calculation ---
    # This should be done after all score updates for the frame (manual, auto, ball)
    # but before drawing the UI elements that display score/EPS.
    current_time_ms = pygame.time.get_ticks()
    if last_eps_calc_time == 0: # Initialize on the first frame
        last_eps_calc_time = current_time_ms

    if current_time_ms - last_eps_calc_time >= eps_calculation_interval:
        time_delta_seconds = (current_time_ms - last_eps_calc_time) / 1000.0
        
        # Calculate EPS based on gross energy earned during the interval
        current_eps = gross_energy_earned_in_interval / time_delta_seconds if time_delta_seconds > 0 else 0.0
        
        gross_energy_earned_in_interval = 0.0 # Reset for the next interval
        last_eps_calc_time = current_time_ms

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
            gross_energy_earned_in_interval += bounce
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
            ball_dy *= -1
            score += bounce
            gross_energy_earned_in_interval += bounce

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

    # --- Show Click Count ---
    click_count_text_surface = font.render("Clicks: " + str(click_count), True, grey)
    click_count_text_rect = click_count_text_surface.get_rect(topright=(width - 10, 10))
    screen.blit(click_count_text_surface, click_count_text_rect)

    # --- Show EPS ---
    eps_text_surface = font.render(f"EPS: {current_eps:.1f}", True, grey)
    # Position it below the click counter, aligned to the right
    eps_text_rect = eps_text_surface.get_rect(topright=(width - 10, click_count_text_rect.bottom + 5))
    screen.blit(eps_text_surface, eps_text_rect)

    pygame.display.flip()

pygame.quit()
