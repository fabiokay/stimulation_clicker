import pygame
import random

# Constants
WIDTH, HEIGHT = 1000, 600
BG_COLOR = (30, 30, 30)
DICE_COLOR = (255, 255, 255)
HELD_COLOR = (200, 200, 0)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 150, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
DICE_SIZE = 60
DICE_GAP = 20
SCORECARD_WIDTH = 300
ROLL_BUTTON_POS = (50, 500)
CATEGORY_FONT_SIZE = 20

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee")


class Die:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
        self.value = 1
        self.held = False

    def roll(self):
        if not self.held:
            self.value = random.randint(1, 6)

    def draw(self, screen):
        color = HELD_COLOR if self.held else DICE_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=2)
        self.draw_dots(screen)

    def draw_dots(self, screen):
        dot_color = TEXT_COLOR
        positions = []
        center = self.rect.center

        if self.value % 2 == 1:
            positions.append(center)
        if self.value > 1:
            positions.append((self.rect.left + 15, self.rect.top + 15))
            positions.append((self.rect.right - 15, self.rect.bottom - 15))
        if self.value > 3:
            positions.append((self.rect.right - 15, self.rect.top + 15))
            positions.append((self.rect.left + 15, self.rect.bottom - 15))
        if self.value == 6:
            positions.append((self.rect.left + 15, center[1]))
            positions.append((self.rect.right - 15, center[1]))

        for pos in positions[:self.value]:
            pygame.draw.circle(screen, dot_color, pos, 5)


def create_dice():
    start_x = 50
    start_y = 100
    return [Die(start_x + i * (DICE_SIZE + DICE_GAP), start_y) for i in range(5)]


def check_three_of_a_kind(dice):
    counts = [dice.count(value) for value in set(dice)]
    return sum(dice) if max(counts) >= 3 else 0


def check_four_of_a_kind(dice):
    counts = [dice.count(value) for value in set(dice)]
    return sum(dice) if max(counts) >= 4 else 0


def check_full_house(dice):
    counts = sorted([dice.count(value) for value in set(dice)], reverse=True)
    return 25 if (len(counts) == 2 and counts[0] == 3 and counts[1] == 2) else 0


def check_small_straight(dice):
    unique = sorted(list(set(dice)))
    for i in range(len(unique) - 3):
        if unique[i + 3] - unique[i] == 3:
            return 30
    return 0


def check_large_straight(dice):
    sorted_dice = sorted(dice)
    return 40 if sorted_dice in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]) else 0


def check_yahtzee(dice):
    return 50 if len(set(dice)) == 1 else 0


def check_chance(dice):
    return sum(dice)


scoring_functions = {
    'Ones': lambda d: sum(x for x in d if x == 1),
    'Twos': lambda d: sum(x for x in d if x == 2),
    'Threes': lambda d: sum(x for x in d if x == 3),
    'Fours': lambda d: sum(x for x in d if x == 4),
    'Fives': lambda d: sum(x for x in d if x == 5),
    'Sixes': lambda d: sum(x for x in d if x == 6),
    'Three of a Kind': check_three_of_a_kind,
    'Four of a Kind': check_four_of_a_kind,
    'Full House': check_full_house,
    'Small Straight': check_small_straight,
    'Large Straight': check_large_straight,
    'Yahtzee': check_yahtzee,
    'Chance': check_chance,
}


def main():
    dice = create_dice()
    categories = [
        {'name': 'Ones', 'score': 0, 'used': False},
        {'name': 'Twos', 'score': 0, 'used': False},
        {'name': 'Threes', 'score': 0, 'used': False},
        {'name': 'Fours', 'score': 0, 'used': False},
        {'name': 'Fives', 'score': 0, 'used': False},
        {'name': 'Sixes', 'score': 0, 'used': False},
        {'name': 'Three of a Kind', 'score': 0, 'used': False},
        {'name': 'Four of a Kind', 'score': 0, 'used': False},
        {'name': 'Full House', 'score': 0, 'used': False},
        {'name': 'Small Straight', 'score': 0, 'used': False},
        {'name': 'Large Straight', 'score': 0, 'used': False},
        {'name': 'Yahtzee', 'score': 0, 'used': False},
        {'name': 'Chance', 'score': 0, 'used': False},
    ]
    category_rects = []
    rolls_left = 3
    current_round = 1
    game_state = "rolling"
    roll_button = pygame.Rect(*ROLL_BUTTON_POS, 100, 40)

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if game_state == "rolling":
                    for die in dice:
                        if die.rect.collidepoint(pos):
                            die.held = not die.held
                    if roll_button.collidepoint(pos) and rolls_left > 0:
                        for die in dice:
                            die.roll()
                        rolls_left -= 1
                        if rolls_left == 0:
                            game_state = "scoring"

                elif game_state == "scoring":
                    for i, rect in enumerate(category_rects):
                        if rect.collidepoint(pos) and not categories[i]['used']:
                            current_dice = [die.value for die in dice]
                            score = scoring_functions[categories[i]['name']](current_dice)
                            categories[i]['score'] = score
                            categories[i]['used'] = True
                            current_round += 1
                            rolls_left = 3
                            game_state = "rolling"
                            for die in dice:
                                die.held = False
                                die.value = 1
                            if current_round > 13:
                                game_state = "game_over"

        # Draw dice
        for die in dice:
            die.draw(screen)

        # Draw roll button
        pygame.draw.rect(screen, BUTTON_COLOR, roll_button, border_radius=5)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Roll ({rolls_left})", True, BUTTON_TEXT_COLOR)
        screen.blit(text, (roll_button.x + 10, roll_button.y + 10))

        # Draw scorecard
        score_x = WIDTH - SCORECARD_WIDTH + 10
        score_y = 50
        category_rects.clear()
        font = pygame.font.Font(None, CATEGORY_FONT_SIZE)

        for i, category in enumerate(categories):
            y = score_y + i * 30
            rect = pygame.Rect(WIDTH - SCORECARD_WIDTH, y, SCORECARD_WIDTH, 25)
            category_rects.append(rect)

            text_color = TEXT_COLOR if not category['used'] else (100, 100, 100)
            text = font.render(f"{category['name']}: {category['score']}", True, text_color)
            screen.blit(text, (score_x, y))

            if game_state == "scoring" and not category['used']:
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)

        # Draw game info
        info_font = pygame.font.Font(None, 24)
        round_text = info_font.render(f"Round: {current_round}/13", True, TEXT_COLOR)
        screen.blit(round_text, (WIDTH - 150, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()