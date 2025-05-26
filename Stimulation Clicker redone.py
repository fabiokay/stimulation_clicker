import pygame
import pygame.mixer
import random # For critical clicks

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
    pygame.mixer.Sound("Audio/Click_6.wav"),
    pygame.mixer.Sound("Audio/Click_7.wav"),
    pygame.mixer.Sound("Audio/Click_8.wav"),
]

sound_upgrade = pygame.mixer.Sound("Audio/Upgrade.wav")
sound_unlock = pygame.mixer.Sound("Audio/Unlock.wav")
sound_supernova = pygame.mixer.Sound("Audio/Supernova.wav")
# Load ball bounce sounds
sound_ball_bounce = [
    pygame.mixer.Sound("Audio/Bounce_1.wav"),
    pygame.mixer.Sound("Audio/Bounce_2.wav"),
    pygame.mixer.Sound("Audio/Bounce_3.wav"),
    pygame.mixer.Sound("Audio/Bounce_4.wav"),
    pygame.mixer.Sound("Audio/Bounce_5.wav"),
    pygame.mixer.Sound("Audio/Bounce_6.wav"),
    pygame.mixer.Sound("Audio/Bounce_7.wav"),
    pygame.mixer.Sound("Audio/Bounce_8.wav"),
    pygame.mixer.Sound("Audio/Bounce_9.wav"),
    pygame.mixer.Sound("Audio/Bounce_10.wav"),
    pygame.mixer.Sound("Audio/Bounce_11.wav"),
    pygame.mixer.Sound("Audio/Bounce_12.wav"),
    pygame.mixer.Sound("Audio/Bounce_13.wav"),
    pygame.mixer.Sound("Audio/Bounce_14.wav"),
    pygame.mixer.Sound("Audio/Bounce_15.wav"),
    pygame.mixer.Sound("Audio/Bounce_16.wav"),
]
# Load background music
pygame.mixer.music.load("Audio/Focus.wav")
pygame.mixer.music.play(-1) # play indefinitely

# --- Colors ---
black = pygame.Color("#141728")
grey  = pygame.Color("#727880") 
violet = pygame.Color("#5C3A93")
petrol = pygame.Color("#387487")
blue = pygame.Color("#59C3C3")
white = pygame.Color("#EBEBEB")
pink = pygame.Color("#D154CA")
dark_slate_gray = pygame.Color("#2F4F4F")
steel_blue = pygame.Color("#4682B4")
olive_drab = pygame.Color("#6B8E23")
coral = pygame.Color("#FF7F50")
khaki = pygame.Color("#994C2C")
teal = pygame.Color("#008080")
medium_purple = pygame.Color("#9370DB")
dark_sea_green = pygame.Color("#8FBC8F")
light_sky_blue = pygame.Color("#87CEFA")
crimson = pygame.Color("#740B20")

# --- Display Setup ---
width, height = 1280, 720
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
pygame.display.set_caption("StImUlAtIoN ClIcKeR")
font = pygame.font.Font("freesansbold.ttf", 14)
framerate = 60

# --- Game Variables ---
#global score
score = 0
click_count = 0 # To count total clicks on the main button
score_value = 1
x2_cost = 100 # Cost for "+1" click upgrade
plus_five_click_cost = 500 # Cost for "+5" click upgrade
plus_ten_click_cost = 2000 # Cost for "+10" click upgrade
plus_twenty_click_cost = 7500 # Cost for "+20" click upgrade
plus_twenty_five_click_cost = 18000 # Cost for "+25" click upgrade
plus_thirty_click_cost = 40000 # Cost for "+30" click upgrade
plus_fifty_click_cost = 90000 # Cost for "+50" click upgrade
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
CRITICAL_FEEDBACK_DURATION = 60 # Frames (e.g., 1 second at 60 FPS)
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
# New variables for Supernova cooldown upgrade
supernova_cooldown_upgrade_cost = 7500  # Initial cost
SUPERNOVA_COOLDOWN_REDUCTION_MS = 10000 # Reduce cooldown by 10 seconds (10000 ms)
MIN_SUPERNOVA_COOLDOWN_MS = 30000       # Minimum cooldown of 30 seconds

# --- EPS (Energy Per Second) Variables ---
current_eps = 0.0
gross_energy_earned_in_interval = 0.0 # Accumulates energy earned for EPS calculation
last_eps_calc_time = 0      # Will be initialized with pygame.time.get_ticks()
eps_calculation_interval = 1000 # milliseconds (e.g., 1 second) # Added from previous diff

# --- Rhythm Bonus Variables ---
RHYTHM_BPM = 60.0
MS_PER_BEAT = (60.0 / RHYTHM_BPM) * 1000.0  # Milliseconds per beat (1000ms for 60 BPM)
RHYTHM_TOLERANCE_MS = 150  # Allowable deviation in ms (+/-)
MIN_RHYTHM_CLICKS_FOR_BONUS = 5
last_main_click_time = 0
consecutive_rhythmic_clicks = 0
RHYTHM_BONUS_MULTIPLIER_PER_TIER = 0.5 # e.g., 25% of score_value per tier
rhythm_feedback_text = ""
rhythm_feedback_timer = 0
RHYTHM_FEEDBACK_DURATION = 90 # Frames (e.g., 1.5 seconds at 60 FPS), slightly longer to see streak
RHYTHM_FEEDBACK_COLOR = blue # Using existing blue color from your color definitions

main_button_visually_pressed = False # For click feedback

# --- Volume Slider for background music Variables ---
music_volume = 0.5  # Initial volume (0.0 to 1.0)
pygame.mixer.music.set_volume(music_volume)
slider_rect = pygame.Rect(width - 200, height - 40, 150, 20) # Track
slider_handle_rect = pygame.Rect(slider_rect.x + music_volume * slider_rect.width - 5, slider_rect.centery - 10, 10, 20) # Handle
slider_dragging = False
volume_slider_font = pygame.font.Font("freesansbold.ttf", 12)

# --- Volume Slider for click sounds Variables ---
click_volume = 0.5  # Initial volume (0.0 to 1.0)
#pygame.mixer.music.set_volume(click_volume)
click_slider_rect = pygame.Rect(width - 200, height - 90, 150, 20) # Track
click_slider_handle_rect = pygame.Rect(click_slider_rect.x + click_volume * click_slider_rect.width - 5, click_slider_rect.centery - 10, 10, 20) # Handle
click_slider_dragging = False
click_volume_slider_font = pygame.font.Font("freesansbold.ttf", 12)

# --- Flags ---
button_x2_visible = False
button_plus_five_click_visible = False
button_plus_ten_click_visible = False
button_plus_twenty_click_visible = False
button_plus_twenty_five_click_visible = False
button_plus_thirty_click_visible = False
button_plus_fifty_click_visible = False
button_auto_visible = False
auto_clicker_active = False
button_buy_ball_visible = False
ball_bought = False
plus_ten_ball_upgrade_unlocked = False # Flag for the +10 ball bounce upgrade
button_crit_chance_upgrade_visible = False
button_crit_multiplier_upgrade_visible = False
critical_hit_unlocked = False # Player starts without critical hits
button_critical_hit_unlock_visible = False
button_supernova_cooldown_upgrade_visible = False

# --- Particle System ---
particles = []
MAX_PARTICLES = 150 # Adjust for performance/density
PARTICLE_SPAWN_RATE_NORMAL = 2 # Particles to spawn per frame normally
PARTICLE_SPAWN_RATE_SUPERNOVA = 7 # Particles to spawn per frame during supernova

class Particle:
    def __init__(self, screen_width, screen_height, is_supernova_particle=False):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.is_supernova_particle = is_supernova_particle

        if self.is_supernova_particle:
            self.size = random.randint(2, 7) # Larger and more varied
            # Brighter colors for supernova
            r = random.randint(180, 255)
            g = random.randint(150, 255)
            b = random.randint(170, 255)
            self.color_base = (r, g, b)
            self.dx = random.uniform(-0.6, 0.6) # Slightly faster/more erratic
            self.dy = random.uniform(-0.5, 0.5)
            self.lifetime = random.randint(150, 300) # Can be similar or slightly longer
            self.max_alpha = 255 # Fully opaque capable
        else:
            self.size = random.randint(1, 3)
            # Original colors
            r = random.randint(60, 120)
            g = random.randint(30, 160)
            b = random.randint(40, 180)
            self.color_base = (r, g, b)
            self.dx = random.uniform(-0.3, 0.3)
            self.dy = random.uniform(-0.2, 0.2) # Slightly slower vertical drift
            self.lifetime = random.randint(120, 300) # 2 to 5 seconds at 60 FPS
            self.max_alpha = 200 # Original max alpha for subtlety

        self.initial_lifetime = float(self.lifetime) # Store as float for division

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        # Optional: Wrap particles around screen edges
        # if self.x > width: self.x = 0
        # if self.x < 0: self.x = width
        # if self.y > height: self.y = 0
        # if self.y < 0: self.y = height

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(self.max_alpha * (self.lifetime / self.initial_lifetime))
            alpha = max(0, min(self.max_alpha, alpha)) # Ensure alpha is within 0-max_alpha
            
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, self.color_base + (alpha,), (self.size, self.size), self.size)
            surface.blit(particle_surf, (self.x - self.size, self.y - self.size))

# --- Ball Properties ---
ball_radius = 15
ball_x, ball_y = width // 2, height // 2
ball_dx, ball_dy = 3, 4
ball_color = petrol # Initial ball color
trail = []

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
    current_spawn_rate = PARTICLE_SPAWN_RATE_SUPERNOVA if supernova_active else PARTICLE_SPAWN_RATE_NORMAL

    # Spawn new particles
    if len(particles) < MAX_PARTICLES:
        for _ in range(current_spawn_rate):
            if len(particles) < MAX_PARTICLES: # Check again in case loop fills it
                particles.append(Particle(width, height, is_supernova_particle=supernova_active))

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
    if score >= 5000: # Unlock for +20 click
        button_plus_twenty_click_visible = True
    if score >= 12000: # Unlock for +25 click
        button_plus_twenty_five_click_visible = True
    if score >= 30000: # Unlock for +30 click
        button_plus_thirty_click_visible = True
    if score >= 70000: # Unlock for +50 click
        button_plus_fifty_click_visible = True
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
    # Visibility for Supernova cooldown upgrade button
    if button_supernova_visible and SUPERNOVA_COOLDOWN_MS > MIN_SUPERNOVA_COOLDOWN_MS:
        button_supernova_cooldown_upgrade_visible = True
    else:
        button_supernova_cooldown_upgrade_visible = False # Hide if supernova not visible or cooldown at min

    # --- Draw Main Button ---
    main_button_original_rect_coords = [x_coord - 50, y_coord - 150, 100, 50]
    main_button_draw_color = grey
    main_button_text_color = black
    
    # Apply visual feedback if pressed
    current_button_rect_list = list(main_button_original_rect_coords) # Make a copy
    current_text_x_offset = 10
    current_text_y_offset = 15

    if main_button_visually_pressed:
        main_button_draw_color = grey.lerp(black, 0.2) # Darken by 20%
        current_button_rect_list[0] += 2 # Offset x
        current_button_rect_list[1] += 2 # Offset y
        # Text position is relative to button's top-left, so it moves with the button

    main_button = pygame.draw.rect(screen, main_button_draw_color, current_button_rect_list, 0, 10)
    main_button_text = font.render("Click me!", True, black)
    screen.blit(main_button_text, (current_button_rect_list[0] + current_text_x_offset, current_button_rect_list[1] + current_text_y_offset))

    # --- Define button layout positions ---
    button_width, button_height = 100, 50
    
    # --- New Column Layout ---
    button_area_top_y = y_coord - 90  # Top Y for the button area in all columns
    VERTICAL_SPACING_IN_COLUMN = 55   # Vertical space between button top-edges in a column
    COLUMN_STRIDE = 220               # Horizontal distance from start of one column to start of next
                                      # (button_width + space for cost text + inter-column gap)

    # Calculate X positions for columns to center the block
    num_columns = 4
    # Total width of the block: (num_columns - 1) strides for the first N-1 columns, 
    # plus the width of the actual button in the last column.
    total_block_width = ( (num_columns - 1) * COLUMN_STRIDE ) + button_width 
    start_x_block = (width - total_block_width) / 2

    col0_x = start_x_block
    col1_x = col0_x + COLUMN_STRIDE
    col2_x = col1_x + COLUMN_STRIDE
    col3_x = col2_x + COLUMN_STRIDE

    button_x2 = None
    button_plus_five_click = None
    button_plus_ten_click = None
    button_plus_twenty_click = None
    button_plus_twenty_five_click = None
    button_plus_thirty_click = None
    button_plus_fifty_click = None
    clicker_auto_button = None
    button_buy_ball = None
    button_plusten_ball = None
    button_auto_power_upgrade = None
    button_auto_speed_upgrade = None
    button_critical_hit_unlock = None
    button_crit_chance_upgrade = None
    button_crit_multiplier_upgrade = None
    button_supernova = None
    button_supernova_cooldown_upgrade = None

    # --- Draw Upgrade Buttons ---
    
    # --- Column 0: Manual Click Upgrades ---
    current_y_col0 = button_area_top_y
    if button_x2_visible:
        button_x2 = pygame.draw.rect(screen, pink, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +1", True, black), (button_x2.x + 10, button_x2.y + 15))
        screen.blit(font.render("Cost: " + str(round(x2_cost)), True, white), (button_x2.right + 10, button_x2.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN
    if button_plus_five_click_visible:
        button_plus_five_click = pygame.draw.rect(screen, blue, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +5", True, black), (button_plus_five_click.x + 10, button_plus_five_click.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_five_click_cost)), True, white), (button_plus_five_click.right + 10, button_plus_five_click.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN
    if button_plus_ten_click_visible:
        button_plus_ten_click = pygame.draw.rect(screen, white, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +10", True, black), (button_plus_ten_click.x + 5, button_plus_ten_click.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_ten_click_cost)), True, white), (button_plus_ten_click.right + 10, button_plus_ten_click.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN
    if button_plus_twenty_click_visible:
        button_plus_twenty_click = pygame.draw.rect(screen, coral, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +20", True, black), (button_plus_twenty_click.x + 5, button_plus_twenty_click.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_twenty_click_cost)), True, white), (button_plus_twenty_click.right + 10, button_plus_twenty_click.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN
    if button_plus_twenty_five_click_visible:
        button_plus_twenty_five_click = pygame.draw.rect(screen, khaki, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +25", True, black), (button_plus_twenty_five_click.x + 5, button_plus_twenty_five_click.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_twenty_five_click_cost)), True, white), (button_plus_twenty_five_click.right + 10, button_plus_twenty_five_click.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN
    if button_plus_thirty_click_visible:
        button_plus_thirty_click = pygame.draw.rect(screen, teal, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +30", True, black), (button_plus_thirty_click.x + 5, button_plus_thirty_click.y + 15)) 
        screen.blit(font.render("Cost: " + str(round(plus_thirty_click_cost)), True, white), (button_plus_thirty_click.right + 10, button_plus_thirty_click.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN
    if button_plus_fifty_click_visible:
        button_plus_fifty_click = pygame.draw.rect(screen, crimson, [col0_x, current_y_col0, button_width, button_height], 0, 10)
        screen.blit(font.render("buy +50", True, white), (button_plus_fifty_click.x + 5, button_plus_fifty_click.y + 15)) 
        screen.blit(font.render("Cost: " + str(round(plus_fifty_click_cost)), True, white), (button_plus_fifty_click.right + 10, button_plus_fifty_click.y + 17))
        current_y_col0 += VERTICAL_SPACING_IN_COLUMN

    # --- Column 1: Unlocks ---
    current_y_col1 = button_area_top_y
    if button_auto_visible and not auto_clicker_active:
        clicker_auto_button = pygame.draw.rect(screen, violet, [col1_x, current_y_col1, button_width, button_height], 0, 10)
        screen.blit(font.render("buy auto", True, black), (clicker_auto_button.x + 10, clicker_auto_button.y + 15))
        screen.blit(font.render("Cost: " + str(auto_clicker_cost), True, white), (clicker_auto_button.right + 10, clicker_auto_button.y + 17))
        current_y_col1 += VERTICAL_SPACING_IN_COLUMN
    if button_buy_ball_visible and not ball_bought:
        button_buy_ball = pygame.draw.rect(screen, petrol, [col1_x, current_y_col1, button_width, button_height], 0, 10)
        screen.blit(font.render("Buy a Ball!", True, black), (button_buy_ball.x + 5, button_buy_ball.y + 15))
        screen.blit(font.render("Cost: 300", True, white), (button_buy_ball.right + 10, button_buy_ball.y + 17))
        current_y_col1 += VERTICAL_SPACING_IN_COLUMN
    if button_critical_hit_unlock_visible and not critical_hit_unlocked:
        button_critical_hit_unlock = pygame.draw.rect(screen, pink, [col1_x, current_y_col1, button_width, button_height], 0, 10)
        screen.blit(font.render("Unlock Crits", True, black), (button_critical_hit_unlock.x + 5, button_critical_hit_unlock.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_hit_unlock_cost)}", True, white), (button_critical_hit_unlock.right + 10, button_critical_hit_unlock.y + 17))
        current_y_col1 += VERTICAL_SPACING_IN_COLUMN

    # --- Column 2: Feature Upgrades ---
    current_y_col2 = button_area_top_y
    if auto_clicker_active: # Auto Power Upgrade
        button_auto_power_upgrade = pygame.draw.rect(screen, violet, [col2_x, current_y_col2, button_width, button_height], 0, 10)
        screen.blit(font.render("Auto Pwr", True, black), (button_auto_power_upgrade.x + 5, button_auto_power_upgrade.y + 15))
        screen.blit(font.render("Cost: " + str(round(auto_power_upgrade_cost)), True, white), (button_auto_power_upgrade.right + 10, button_auto_power_upgrade.y + 17))
        current_y_col2 += VERTICAL_SPACING_IN_COLUMN
    if auto_clicker_active: # Auto Speed Upgrade
        button_auto_speed_upgrade = pygame.draw.rect(screen, violet, [col2_x, current_y_col2, button_width, button_height], 0, 10)
        screen.blit(font.render("Auto Spd", True, black), (button_auto_speed_upgrade.x + 5, button_auto_speed_upgrade.y + 15))
        screen.blit(font.render("Cost: " + str(round(auto_speed_upgrade_cost)), True, white), (button_auto_speed_upgrade.right + 10, button_auto_speed_upgrade.y + 17))
        current_y_col2 += VERTICAL_SPACING_IN_COLUMN
    if ball_bought and plus_ten_ball_upgrade_unlocked:
        button_plusten_ball = pygame.draw.rect(screen, white, [col2_x, current_y_col2, button_width, button_height], 0, 10)
        screen.blit(font.render("+10 Ball!", True, black), (button_plusten_ball.x + 5, button_plusten_ball.y + 15))
        screen.blit(font.render("Cost: " + str(round(plus_ten_ball_cost)), True, white), (button_plusten_ball.right + 10, button_plusten_ball.y + 17))
        current_y_col2 += VERTICAL_SPACING_IN_COLUMN
    if critical_hit_unlocked and button_crit_chance_upgrade_visible: 
        button_crit_chance_upgrade = pygame.draw.rect(screen, pink, [col2_x, current_y_col2, button_width, button_height], 0, 10)
        screen.blit(font.render("Crit Chance+", True, black), (button_crit_chance_upgrade.x + 5, button_crit_chance_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_chance_upgrade_cost)}", True, white), (button_crit_chance_upgrade.right + 10, button_crit_chance_upgrade.y + 17))
        screen.blit(font.render(f"({CRITICAL_CHANCE*100:.0f}%)", True, white), (button_crit_chance_upgrade.x + 20, button_crit_chance_upgrade.y - 15))
        current_y_col2 += VERTICAL_SPACING_IN_COLUMN
    if critical_hit_unlocked and button_crit_multiplier_upgrade_visible:
        button_crit_multiplier_upgrade = pygame.draw.rect(screen, pink, [col2_x, current_y_col2, button_width, button_height], 0, 10)
        screen.blit(font.render("Crit Multi+", True, black), (button_crit_multiplier_upgrade.x + 5, button_crit_multiplier_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(critical_multiplier_upgrade_cost)}", True, white), (button_crit_multiplier_upgrade.right + 10, button_crit_multiplier_upgrade.y + 17))
        screen.blit(font.render(f"(x{CRITICAL_MULTIPLIER:.1f})", True, white), (button_crit_multiplier_upgrade.x + 25, button_crit_multiplier_upgrade.y - 15))
        current_y_col2 += VERTICAL_SPACING_IN_COLUMN
    if button_supernova_cooldown_upgrade_visible: 
        button_supernova_cooldown_upgrade = pygame.draw.rect(screen, blue, [col2_x, current_y_col2, button_width, button_height], 0, 10)
        screen.blit(font.render("Nova CD-", True, black), (button_supernova_cooldown_upgrade.x + 10, button_supernova_cooldown_upgrade.y + 15))
        screen.blit(font.render(f"Cost: {round(supernova_cooldown_upgrade_cost)}", True, white), (button_supernova_cooldown_upgrade.right + 10, button_supernova_cooldown_upgrade.y + 17))
        reduction_text = f"(-{SUPERNOVA_COOLDOWN_REDUCTION_MS/1000:.0f}s)"
        screen.blit(font.render(reduction_text, True, white), (button_supernova_cooldown_upgrade.x + 20, button_supernova_cooldown_upgrade.y - 15))
        current_y_col2 += VERTICAL_SPACING_IN_COLUMN

    # --- Column 3: Supernova ---
    current_y_col3 = button_area_top_y
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
        button_supernova = pygame.draw.rect(screen, button_color, [col3_x, current_y_col3, button_width, button_height], 0, 10)
        supernova_text_render = font.render(supernova_text_str, True, black if supernova_active or supernova_ready else white) # Text color contrast
        text_rect_supernova = supernova_text_render.get_rect(center=button_supernova.center)
        screen.blit(supernova_text_render, text_rect_supernova)
        current_y_col3 += VERTICAL_SPACING_IN_COLUMN

    # --- Draw Rhythm Feedback ---
    if rhythm_feedback_timer > 0:
        rhythm_text_surface = font.render(rhythm_feedback_text, True, RHYTHM_FEEDBACK_COLOR)
        # Position it near the critical feedback, perhaps slightly offset or different side
        rhythm_text_rect = rhythm_text_surface.get_rect(center=(main_button.centerx, main_button.top - 40)) # Adjust Y as needed
        screen.blit(rhythm_text_surface, rhythm_text_rect)
        rhythm_feedback_timer -= 1


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

    # --- Volume Slider Logic background music---
    # Draw slider
    pygame.draw.rect(screen, grey, slider_rect, 0, 5)
    pygame.draw.rect(screen, blue, slider_handle_rect, 0, 3)
    volume_text = volume_slider_font.render(f"Music Vol: {int(music_volume * 100)}%", True, white)
    screen.blit(volume_text, (slider_rect.x, slider_rect.y - 20))

    # Update handle position based on current music_volume (in case it's set elsewhere)
    slider_handle_rect.centerx = slider_rect.x + music_volume * slider_rect.width
    # Ensure handle stays within slider bounds (important if volume is set programmatically)
    slider_handle_rect.centerx = max(slider_rect.left + slider_handle_rect.width // 2, min(slider_rect.right - slider_handle_rect.width // 2, slider_handle_rect.centerx))

    # --- Volume Slider Logic click sounds ---
    # Draw slider
    pygame.draw.rect(screen, grey, click_slider_rect, 0, 5)
    pygame.draw.rect(screen, blue, click_slider_handle_rect, 0, 3)
    click_volume_text = click_volume_slider_font.render(f"Click Vol: {int(click_volume * 100)}%", True, white)
    screen.blit(click_volume_text, (click_slider_rect.x, click_slider_rect.y - 20))

    # Update handle position based on current click_volume (in case it's set elsewhere)
    click_slider_handle_rect.centerx = click_slider_rect.x + click_volume * click_slider_rect.width
    # Ensure handle stays within slider bounds (important if volume is set programmatically)
    click_slider_handle_rect.centerx = max(click_slider_rect.left + click_slider_handle_rect.width // 2, min(click_slider_rect.right - click_slider_handle_rect.width // 2, click_slider_handle_rect.centerx))



    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for main button press for visual feedback
            if main_button.collidepoint(event.pos): # Check against the drawn rect of the button
                main_button_visually_pressed = True
            
            # Volume Slider Music 
            if slider_rect.collidepoint(event.pos) or slider_handle_rect.collidepoint(event.pos):
                slider_dragging = True
                # Immediately update volume on click
                mouse_x, _ = event.pos
                # Calculate new volume based on click position relative to slider track
                new_volume = (mouse_x - slider_rect.x) / slider_rect.width
                music_volume = max(0.0, min(1.0, new_volume)) # Clamp between 0 and 1
                pygame.mixer.music.set_volume(music_volume)
                slider_handle_rect.centerx = slider_rect.x + music_volume * slider_rect.width
                # Clamp handle position
                slider_handle_rect.centerx = max(slider_rect.left + slider_handle_rect.width // 2, min(slider_rect.right - slider_handle_rect.width // 2, slider_handle_rect.centerx))

            # Click Volume Slider Click
            if click_slider_rect.collidepoint(event.pos) or click_slider_handle_rect.collidepoint(event.pos):
                click_slider_dragging = True
                # Immediately update volume on click
                mouse_x, _ = event.pos
                # Calculate new volume based on click position relative to slider track
                click_new_volume = (mouse_x - click_slider_rect.x) / click_slider_rect.width
                click_volume = max(0.0, min(1.0, click_new_volume)) # Clamp between 0 and 1
                # pygame.mixer.music.set_volume(click_volume) # THIS WAS THE CULPRIT!
                click_slider_handle_rect.centerx = click_slider_rect.x + click_volume * click_slider_rect.width
                # Clamp handle position
                click_slider_handle_rect.centerx = max(click_slider_rect.left + click_slider_handle_rect.width // 2, min(click_slider_rect.right - click_slider_handle_rect.width // 2, click_slider_handle_rect.centerx))

            if main_button.collidepoint(event.pos):
                current_click_time_for_rhythm = pygame.time.get_ticks()
                base_click_value_for_this_click = score_value
                score_to_add_this_click = 0 # Initialize score to add for this specific click event

                if supernova_active:
                    base_click_value_for_this_click *= SUPERNOVA_CLICK_MULTIPLIER

                if critical_hit_unlocked: # Only check for crits if unlocked
                    if random.random() < CRITICAL_CHANCE:
                        # Critical Hit!
                        crit_amount = base_click_value_for_this_click * CRITICAL_MULTIPLIER
                        score_to_add_this_click = crit_amount # Crit overrides base
                        critical_feedback_text = f"CRITICAL! +{round(crit_amount)}"
                        critical_feedback_timer = CRITICAL_FEEDBACK_DURATION
                    else:
                        # Normal Click (Supernova-boosted if active)
                        score_to_add_this_click = base_click_value_for_this_click
                else: # If crits not unlocked, always a normal click
                    score_to_add_this_click = base_click_value_for_this_click # (Supernova-boosted if active)
                
                score += score_to_add_this_click
                gross_energy_earned_in_interval += score_to_add_this_click
                click_count += 1 # Increment click counter
                #random.choice(click_sounds).play() # Play a randomly chosen click sound
                chosen_click_sound = random.choice(click_sounds)
                chosen_click_sound.set_volume(click_volume) # Apply the click_volume
                chosen_click_sound.play()

                # Rhythm Bonus Logic
                if last_main_click_time == 0: # First click in a potential sequence
                    consecutive_rhythmic_clicks = 1
                else:
                    time_diff = current_click_time_for_rhythm - last_main_click_time
                    if abs(time_diff - MS_PER_BEAT) <= RHYTHM_TOLERANCE_MS:
                        consecutive_rhythmic_clicks += 1
                    else: # Rhythm broken
                        consecutive_rhythmic_clicks = 1 # Current click starts a new sequence of 1
                last_main_click_time = current_click_time_for_rhythm

                if consecutive_rhythmic_clicks >= MIN_RHYTHM_CLICKS_FOR_BONUS:
                    bonus_tier = consecutive_rhythmic_clicks - (MIN_RHYTHM_CLICKS_FOR_BONUS - 1)
                    actual_rhythm_bonus = (score_value * RHYTHM_BONUS_MULTIPLIER_PER_TIER) * bonus_tier
                    
                    score += actual_rhythm_bonus
                    gross_energy_earned_in_interval += actual_rhythm_bonus
                    
                    rhythm_feedback_text = f"Rhythm x{consecutive_rhythmic_clicks}! +{round(actual_rhythm_bonus)}"
                    rhythm_feedback_timer = RHYTHM_FEEDBACK_DURATION
                elif consecutive_rhythmic_clicks > 1: # Show streak even before bonus
                    rhythm_feedback_text = f"Rhythm x{consecutive_rhythmic_clicks}"
                    rhythm_feedback_timer = RHYTHM_FEEDBACK_DURATION
                # If consecutive_rhythmic_clicks is 1, any existing rhythm_feedback_timer will continue to count down.
            
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
            
            if button_plus_twenty_click and button_plus_twenty_click.collidepoint(event.pos) and score >= plus_twenty_click_cost:
                score -= plus_twenty_click_cost
                score_value += 20
                plus_twenty_click_cost *= 1.9 
                sound_upgrade.play()

            if button_plus_twenty_five_click and button_plus_twenty_five_click.collidepoint(event.pos) and score >= plus_twenty_five_click_cost:
                score -= plus_twenty_five_click_cost
                score_value += 25
                plus_twenty_five_click_cost *= 2.0
                sound_upgrade.play()

            if button_plus_thirty_click and button_plus_thirty_click.collidepoint(event.pos) and score >= plus_thirty_click_cost:
                score -= plus_thirty_click_cost
                score_value += 30
                plus_thirty_click_cost *= 2.1
                sound_upgrade.play()

            if button_plus_fifty_click and button_plus_fifty_click.collidepoint(event.pos) and score >= plus_fifty_click_cost:
                score -= plus_fifty_click_cost
                score_value += 50
                plus_fifty_click_cost *= 2.2
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

            if button_supernova_cooldown_upgrade and button_supernova_cooldown_upgrade.collidepoint(event.pos) and score >= supernova_cooldown_upgrade_cost:
                if SUPERNOVA_COOLDOWN_MS > MIN_SUPERNOVA_COOLDOWN_MS:
                    score -= supernova_cooldown_upgrade_cost
                    SUPERNOVA_COOLDOWN_MS = max(MIN_SUPERNOVA_COOLDOWN_MS, SUPERNOVA_COOLDOWN_MS - SUPERNOVA_COOLDOWN_REDUCTION_MS)
                    supernova_cooldown_upgrade_cost *= 1.8 # Increase cost for the next upgrade
                    sound_upgrade.play()
                    if SUPERNOVA_COOLDOWN_MS <= MIN_SUPERNOVA_COOLDOWN_MS:
                        button_supernova_cooldown_upgrade_visible = False # Hide button if min cooldown reached


        elif event.type == AUTO_CLICK_EVENT and auto_clicker_active:
            score += auto_click_power
            gross_energy_earned_in_interval += auto_click_power

        elif event.type == pygame.MOUSEBUTTONUP:
            if main_button_visually_pressed: # Reset visual feedback for main button
                main_button_visually_pressed = False
            if slider_dragging:
                slider_dragging = False
            if click_slider_dragging:
                click_slider_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, _ = event.pos # Get mouse position once for this motion event

            # slider dragging logic for background music volume
            if slider_dragging:
                new_volume = (mouse_x - slider_rect.x) / slider_rect.width
                music_volume = max(0.0, min(1.0, new_volume)) # Clamp between 0 and 1
                pygame.mixer.music.set_volume(music_volume)
                slider_handle_rect.centerx = slider_rect.x + music_volume * slider_rect.width
                slider_handle_rect.centerx = max(slider_rect.left + slider_handle_rect.width // 2, min(slider_rect.right - slider_handle_rect.width // 2, slider_handle_rect.centerx))
            
            # slider dragging logic for click sounds volume
            if click_slider_dragging:
                click_new_volume = (mouse_x - click_slider_rect.x) / click_slider_rect.width
                click_volume = max(0.0, min(1.0, click_new_volume)) # Clamp between 0 and 1
                #pygame.mixer.music.set_volume(click_volume)
                click_slider_handle_rect.centerx = click_slider_rect.x + click_volume * click_slider_rect.width
                click_slider_handle_rect.centerx = max(click_slider_rect.left + click_slider_handle_rect.width // 2, min(click_slider_rect.right - click_slider_handle_rect.width // 2, click_slider_handle_rect.centerx))



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
        if len(trail) > bounce: # Use bounce value for trail length
            trail.pop(0)

        # Bounce and score
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
            ball_dx *= -1
            score += bounce
            ball_color = random.choice([violet, petrol, blue, pink, coral, khaki, teal, medium_purple, dark_sea_green, light_sky_blue, crimson, white]) # Change color on bounce
            random.choice(sound_ball_bounce).play() # Play a random bounce sound
            gross_energy_earned_in_interval += bounce
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
            ball_dy *= -1
            score += bounce
            gross_energy_earned_in_interval += bounce
            ball_color = random.choice([violet, petrol, blue, pink, coral, khaki, teal, medium_purple, dark_sea_green, light_sky_blue, crimson, white]) # Change color on bounce
            random.choice(sound_ball_bounce).play() # Play a random bounce sound

        # Draw trail
        for i, (tx, ty) in enumerate(trail):
            fade = int(255 * (i + 1) / bounce) # Use bounce value for fade calculation
            # Use the current ball_color's RGB values and apply the fade alpha
            current_trail_r = ball_color.r
            current_trail_g = ball_color.g
            current_trail_b = ball_color.b
            trail_color = (current_trail_r, current_trail_g, current_trail_b, fade)
            trail_surf = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, trail_color, (ball_radius, ball_radius), ball_radius)
            screen.blit(trail_surf, (tx - ball_radius, ty - ball_radius))

        # Draw Ball
        pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

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
