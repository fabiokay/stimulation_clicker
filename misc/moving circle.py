# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

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

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_radius = 10

# --- Particle Setup ---
class Particle:
    def __init__(self, start_pos, target_pos, color=white, speed=450, radius=4):
        self.pos = pygame.Vector2(start_pos) # Start at a copy of the player's position
        self.radius = radius
        self.color = color
        self.speed = speed
        # Calculate direction towards the target's position at the moment of firing
        if (target_pos - start_pos).length_squared() > 0:
            self.direction = (target_pos - start_pos).normalize()
        else:
            self.direction = pygame.Vector2(0, -1) # Default upwards if target is at start_pos

    def update(self, dt):
        self.pos += self.direction * self.speed * dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def is_offscreen(self, screen_width, screen_height):
        return (self.pos.x < -self.radius or self.pos.x > screen_width + self.radius or
                self.pos.y < -self.radius or self.pos.y > screen_height + self.radius)


# --- Enemy Triangle Setup ---
class EnemyTriangle:
    def __init__(self, screen_width, screen_height):
        self.height = 20  # Length from tip to middle of base
        self.base_width = 15  # Full width of the base
        self.speed = random.uniform(70, 110)  # Pixels per second
        self.color = olive_drab # You can pick any color or randomize it

        # Spawn on a random edge, with the tip (self.pos) starting off-screen
        edge = random.choice(["top", "bottom", "left", "right"])
        margin = self.height # Ensure it spawns fully off-screen

        if edge == "top":
            self.pos = pygame.Vector2(random.uniform(0, screen_width), -margin)
        elif edge == "bottom":
            self.pos = pygame.Vector2(random.uniform(0, screen_width), screen_height + margin)
        elif edge == "left":
            self.pos = pygame.Vector2(-margin, random.uniform(0, screen_height))
        else:  # right
            self.pos = pygame.Vector2(screen_width + margin, random.uniform(0, screen_height))

    def update(self, target_pos, dt):
        # Move towards the target_pos
        if (target_pos - self.pos).length_squared() > 0:  # Avoid division by zero if already at target
            direction = (target_pos - self.pos).normalize()
            self.pos += direction * self.speed * dt

    def draw(self, surface, target_pos):
        # Calculate direction vector towards target for orientation
        direction_to_target = pygame.Vector2(0, -1) # Default if on top of target (e.g., point "up")
        if (target_pos - self.pos).length_squared() > 0:
            direction_to_target = (target_pos - self.pos).normalize()

        # p1 is the tip of the triangle, which is self.pos
        p1 = self.pos

        # Calculate center of the base (behind the tip)
        base_center = self.pos - direction_to_target * self.height
        # Calculate perpendicular vector for the base spread
        perp_vector = pygame.Vector2(-direction_to_target.y, direction_to_target.x)
        p2 = base_center + perp_vector * (self.base_width / 2)
        p3 = base_center - perp_vector * (self.base_width / 2)
        pygame.draw.polygon(surface, self.color, [p1, p2, p3])


enemies = []
enemy_spawn_timer = 0.0
ENEMY_SPAWN_INTERVAL = 1.5  # Seconds between spawns
MAX_ENEMIES = 100 # Maximum number of enemies on screen

particles = []
SHOOT_COOLDOWN = 0.25  # Seconds
last_shot_time = 0.0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(petrol)

    movement_speed = 200
    move_vector = pygame.Vector2(0, 0)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_vector.y -= 1
    if keys[pygame.K_s]:
        move_vector.y += 1
    if keys[pygame.K_a]:
        move_vector.x -= 1
    if keys[pygame.K_d]:
        move_vector.x += 1

    if move_vector.length_squared() > 0: # Check if there's any movement
        move_vector.normalize_ip() # Normalize to make length 1
        player_pos += move_vector * movement_speed * dt

    # --- Shooting Logic ---
    current_time = pygame.time.get_ticks() / 1000.0 # Current time in seconds
    if keys[pygame.K_SPACE] and (current_time - last_shot_time > SHOOT_COOLDOWN):
        if enemies: # Only shoot if there are enemies
            last_shot_time = current_time
            # Find nearest enemy
            nearest_enemy = None
            min_dist_sq = float('inf')
            for enemy in enemies:
                dist_sq = (enemy.pos - player_pos).length_squared()
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    nearest_enemy = enemy
            
            if nearest_enemy:
                particles.append(Particle(player_pos, nearest_enemy.pos, color=light_sky_blue))

    # --- Enemy Spawning ---
    enemy_spawn_timer += dt
    if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL and len(enemies) < MAX_ENEMIES:
        enemy_spawn_timer = 0  # Reset timer
        new_enemy = EnemyTriangle(screen.get_width(), screen.get_height())
        enemies.append(new_enemy)
    
    # --- Update and Draw Particles ---
    # Iterate over a copy for safe removal
    for particle in particles[:]:
        particle.update(dt)
        if particle.is_offscreen(screen.get_width(), screen.get_height()):
            particles.remove(particle)
        else:
            particle.draw(screen)

    # --- Enemy Update and Draw ---
    # Iterate over a copy for safe removal
    for enemy in enemies[:]: # Iterate over a copy for safe removal
        enemy.update(player_pos, dt) # player_pos is the target
        enemy.draw(screen, player_pos) # Pass player_pos for orientation

    # --- Collision Detection (Particle vs Enemy) ---
    for particle in particles[:]:
        for enemy in enemies[:]:
            # Simple distance check: particle center to enemy tip
            if (particle.pos - enemy.pos).length_squared() < (particle.radius + enemy.height * 0.5)**2: # enemy.height * 0.5 is a rough collision radius for the triangle
                particles.remove(particle)
                enemies.remove(enemy)
                break # Particle can only hit one enemy, and is now gone

    # --- Boundary Checks ---
    # Keep player on screen
    if player_pos.x - player_radius < 0:
        player_pos.x = player_radius
    if player_pos.x + player_radius > screen.get_width():
        player_pos.x = screen.get_width() - player_radius
    if player_pos.y - player_radius < 0:
        player_pos.y = player_radius
    if player_pos.y + player_radius > screen.get_height():
        player_pos.y = screen.get_height() - player_radius

    # --- Draw everything ---
    # Draw player on top of particles and enemies
    pygame.draw.circle(screen, crimson, player_pos, player_radius)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()