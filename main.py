import pygame
import random
import os

current_dir = os.path.dirname(__file__)
background_image_path = os.path.join(current_dir, "background.png")
box_image_path = os.path.join(current_dir, "box.png")
font_path = os.path.join(current_dir, "Lato\Lato-Bold.ttf")
sound_path = os.path.join(current_dir, "clicksfx.mp3")
main_menu_path = os.path.join(current_dir, "main_menu.png")
help_menu_path = os.path.join(current_dir, "help_menu.png")
gameover_menu_path = os.path.join(current_dir, "gameover_menu.png")
difficulty_menu_path = os.path.join(current_dir, "difficulty_menu.png")

#Variables
cards_count = 16
moves = 0
misses = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CARD_WIDTH = 100
CARD_HEIGHT = 100
ROWS = 4
COLS = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

#Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mix & match")
clock = pygame.time.Clock()

#Images
background_image = pygame.image.load(background_image_path)
box_image = pygame.image.load(box_image_path).convert_alpha()
box_image = pygame.transform.scale(box_image, (CARD_WIDTH, CARD_HEIGHT))
main_menu_image = pygame.image.load(main_menu_path)
help_menu_image = pygame.image.load(help_menu_path)
difficulty_menu_image = pygame.image.load(difficulty_menu_path)
gameover_menu_image = pygame.image.load(gameover_menu_path)

#Buttons
start_button_rect = pygame.Rect(183, 299, 203, 203)
help_button_rect = pygame.Rect(413, 299, 203, 203)
help_back_button_rect = pygame.Rect(528, 502, 129, 46)
menu_back_fromEnd = pygame.Rect(187, 525, 129, 46)
retry_fromEnd = pygame.Rect(484, 525, 129, 46)
DIFFICULTY_hard = pygame.Rect(181, 325, 143, 203)
DIFFICULTY_medium= pygame.Rect(334, 325, 143, 203)
DIFFICULTY_easy= pygame.Rect(487, 325, 143, 203)
menu_fromGame= pygame.Rect(324, 55, 152, 46)

custom_font = pygame.font.Font(font_path, 40)
click_sound = pygame.mixer.Sound(sound_path)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

def main_menu():
    screen.blit(main_menu_image, (0, 0))

def help_menu():
    screen.blit(help_menu_image, (0, 0))

def difficulty_menu():
    screen.blit(difficulty_menu_image, (0, 0))

def gameover_menu():
    screen.blit(gameover_menu_image, (0, 0))
    moves_text = custom_font.render(f"Moves: {moves}", True, WHITE)
    moves_text_rect = moves_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    
    misses_text = custom_font.render(f"Misses: {misses}", True, WHITE)
    misses_text_rect = misses_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    
    screen.blit(moves_text, moves_text_rect)
    screen.blit(misses_text, misses_text_rect)

current_state = main_menu

def game_menu():

    global cards_count

    if cards_count % 4 == 0:
        ROWS = cards_count // 4
        COLS = 4
    else:
        ROWS = cards_count // 4 + 1
        COLS = cards_count // ROWS

    cards_total = ROWS * COLS

    start_x = (SCREEN_WIDTH - (CARD_WIDTH + 10) * COLS) // 2
    start_y = (SCREEN_HEIGHT - (CARD_HEIGHT + 10) * ROWS) // 2

    card_values = LinkedList()

    numbers = [i for i in range(1, (cards_total // 2) + 1)] * 2
    random.shuffle(numbers)

    for num in numbers:
        card_values.insert(num)

    cards = []
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(start_x + col * (CARD_WIDTH + 10), start_y + row * (CARD_HEIGHT + 10), CARD_WIDTH, CARD_HEIGHT)
            cards.append((rect, False, card_values.head.data))
            card_values.head = card_values.head.next

    opened_cards = []
    global moves
    global misses
    global current_state
    moves=0
    misses = 0
    game_over = False
    game_to_menu = False

    while not game_over:    
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_fromGame.collidepoint(event.pos):
                    game_to_menu = True
                    break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (rect, flipped, value) in enumerate(cards):
                    if rect.collidepoint(event.pos) and not flipped:
                        click_sound.play()

                        if len(opened_cards) < 3:
                            cards[i] = (rect, True, value)
                            opened_cards.append((i, value))

                            if len(opened_cards) == 3:
                                moves += 1
                                value1 = opened_cards[0][1]
                                value2 = opened_cards[1][1]
                                value3 = opened_cards[2][1]
                                if (value1 != value3 or value2 != value3) and (value1 != value2):
                                    for idx, val in opened_cards[:2]:
                                        cards[idx] = (cards[idx][0], False, cards[idx][2])
                                    misses += 1

                                opened_cards = [(i, value3)]

        for rect, flipped, value in cards:
            if flipped:
                number_box = os.path.join(current_dir, str(value) + ".png")
                number_box = pygame.image.load(number_box).convert_alpha()
                number_box = pygame.transform.scale(number_box, (CARD_WIDTH, CARD_HEIGHT))
                screen.blit(number_box, rect)
            else:
                screen.blit(box_image, rect)

        moves_text = custom_font.render(f"Moves: {moves}", True, WHITE)
        misses_text = custom_font.render(f"Misses: {misses}", True, WHITE)
        screen.blit(moves_text, (40, 30))
        screen.blit(misses_text, (40, 80))

        all_opened = all(flipped for _, flipped, _ in cards)
        if all_opened:
            current_state = gameover_menu
            break

        if game_to_menu:
            current_state = main_menu
            break

        pygame.display.flip()
        clock.tick(30)

    return main_menu

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if current_state == difficulty_menu:
                if DIFFICULTY_hard.collidepoint(event.pos):
                    cards_count = 20
                    current_state = game_menu
                if DIFFICULTY_medium.collidepoint(event.pos):
                    cards_count = 16
                    current_state = game_menu
                if DIFFICULTY_easy.collidepoint(event.pos):
                    cards_count = 12
                    current_state = game_menu

            if current_state == game_menu:
                if menu_fromGame.collidepoint(event.pos):
                    current_state = main_menu

            if current_state == main_menu:
                if start_button_rect.collidepoint(event.pos):
                    current_state = difficulty_menu
                if help_button_rect.collidepoint(event.pos):
                    current_state = help_menu
            
            if current_state == help_menu:
                if help_back_button_rect.collidepoint(event.pos):
                    current_state = main_menu

            if current_state == gameover_menu:
                if menu_back_fromEnd.collidepoint(event.pos):
                    current_state = main_menu
                if retry_fromEnd.collidepoint(event.pos):
                    current_state = game_menu

    current_state()
    pygame.display.flip()
    clock.tick(30)