import pygame
import random
import os

current_dir = os.path.dirname(__file__)
background_image_path = os.path.join(current_dir, "background.png")
box_image_path = os.path.join(current_dir, "box.png")
font_path = os.path.join(current_dir, "Gamer.ttf")
sound_path = os.path.join(current_dir, "clicksfx.mp3")

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

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mix & match")

clock = pygame.time.Clock()

background_image = pygame.image.load(background_image_path)
box_image = pygame.image.load(box_image_path).convert_alpha()
box_image = pygame.transform.scale(box_image, (CARD_WIDTH, CARD_HEIGHT))
custom_font = pygame.font.Font(font_path, 57)
click_sound = pygame.mixer.Sound(sound_path)

numbers = [i for i in range(1, (ROWS * COLS) // 2 + 1)] * 2
random.shuffle(numbers)

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

card_values = LinkedList()
for num in numbers:
    card_values.insert(num)

start_x = (SCREEN_WIDTH - (CARD_WIDTH + 10) * COLS) // 2
start_y = (SCREEN_HEIGHT - (CARD_HEIGHT + 10) * ROWS) // 2

cards = []
for row in range(ROWS):
    for col in range(COLS):
        rect = pygame.Rect(start_x + col * (CARD_WIDTH + 10), start_y + row * (CARD_HEIGHT + 10), CARD_WIDTH, CARD_HEIGHT)
        cards.append((rect, False, card_values.head.data))
        card_values.head = card_values.head.next

opened_cards = []
moves = 0
misses = 0
game_over = False

running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
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
    screen.blit(moves_text, (20, 20))
    screen.blit(misses_text, (20, 60))

    all_opened = all(flipped for _, flipped, _ in cards)
    if all_opened:
        game_over = True

    if game_over:
        game_over_text = custom_font.render("Congratulations! Game Over!", True, GREEN)
        result_text = custom_font.render(f"You got {misses} misses on {moves} moves!", True, GREEN)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2))
        screen.blit(result_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
