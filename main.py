import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 100
ROWS = 4
COLS = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

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

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")

clock = pygame.time.Clock()

numbers = [i for i in range(1, (ROWS * COLS) // 2 + 1)] * 2
random.shuffle(numbers)

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

font = pygame.font.Font(None, 24)

game_over = False

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            for i, (rect, flipped, value) in enumerate(cards):
                if rect.collidepoint(event.pos) and not flipped:
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
            pygame.draw.rect(screen, GRAY, rect)
            text = font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, BLACK, rect)

    moves_text = font.render(f"Moves: {moves}", True, BLACK)
    misses_text = font.render(f"Misses: {misses}", True, BLACK)
    screen.blit(moves_text, (20, SCREEN_HEIGHT - 30))
    screen.blit(misses_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30))

    all_opened = all(flipped for _, flipped, _ in cards)
    if all_opened:
        game_over = True

    if game_over:
        game_over_text = font.render("Congratulations! Game Over!", True, GREEN)
        result_text = font.render(f"You got {misses} misses on {moves} moves!", True, GREEN)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        screen.blit(result_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()