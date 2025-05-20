import pygame
import sys

pygame.init()

# Setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker + Ball")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Score
score = 0

# Buttons
main_button = pygame.Rect(150, 120, 100, 50)
buy_button = pygame.Rect(150, 200, 100, 50)
button2_visible = True
auto_clicker_active = False

# Ball
ball_radius = 15
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 3, 3

# Auto-clicker
AUTO_CLICK_EVENT = pygame.USEREVENT + 1
AUTO_CLICK_DELAY = 1000

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if main_button.collidepoint(event.pos):
                score += 1

            if button2_visible and buy_button.collidepoint(event.pos):
                button2_visible = False
                auto_clicker_active = True
                pygame.time.set_timer(AUTO_CLICK_EVENT, AUTO_CLICK_DELAY)

        if event.type == AUTO_CLICK_EVENT and auto_clicker_active:
            score += 1

    # --- Ball Movement ---
    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx *= -1
        score += 10
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_dy *= -1
        score += 10

    # --- Drawing ---
    screen.fill((30, 30, 30))

    # Ball
    pygame.draw.circle(screen, (255, 100, 100), (ball_x, ball_y), ball_radius)

    # Buttons
    pygame.draw.rect(screen, (70, 130, 180), main_button)
    screen.blit(font.render("Click Me!", True, (255, 255, 255)), (main_button.x + 10, main_button.y + 10))

    if button2_visible:
        pygame.draw.rect(screen, (0, 200, 100), buy_button)
        screen.blit(font.render("Buy", True, (0, 0, 0)), (buy_button.x + 25, buy_button.y + 10))

    # Score
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
