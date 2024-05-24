import socket
import pygame
import random

from SetOfCards import SetOfCards


IP = '127.0.0.1'
PORT = 1729
WINDOW_WIDTH = 1373
WINDOW_HEIGHT = 810
WHITE = (255, 255, 255)
COLOR_KEY = 154, 102, 10
BACKGROUND = 'CatBackground.jpg'
CAT = ["Cat0.png", "Cat1.png", "Cat2.png", "Cat3.png", "Cat4.png", "Cat5.png", "Cat6.png", "Cat7.png", "Cat8.png", "Cat9.png", "CatPeek.png", "CatDraw2.png", "CatBlank.png"]
CARD_WIDTH = 181
CARD_HEIGHT = 240
CAT12= 'CatBackCard.png'
used_cards = [12]
back_card_rect=pygame.Rect(400, 200, CARD_WIDTH, CARD_HEIGHT)
card_rects = []
#card_rects = [(280, 540, 181, 240), (480, 540, 181, 240), (680, 540, 181, 240), (880, 540, 181, 240)]
#card_rects = [<rect(280, 540, 181, 240)>, <rect(480, 540, 181, 240)>, <rect(680, 540, 181, 240)>, <rect(880, 540, 181, 240)>, <rect(280, 540, 181, 240)>, <rect(480, 540, 181, 240)>, <rect(680, 540, 181, 240)>, <rect(880, 540, 181, 240)>]
current_card = 0
show_new_card = False
#the amount of every card in the stack
numbers = [i for i in range(7)] * 4 + [7, 8] * 5 + [9] * 7 + [10, 10, 10, 11, 11, 11]
selected_numbers = random.sample(numbers, 4)
set_of_cards = SetOfCards(selected_numbers)
for number in selected_numbers:
    numbers.remove(number)
pygame.init()
 #fgh
def create_new_screen(screen):
    global card_rects
    pygame.display.set_caption("RatATat")
    background = pygame.image.load(BACKGROUND)
    screen.blit(background, (0, 0))
    #pygame.display.flip()
    cat_back_card = pygame.image.load(CAT12)
    cat_back_card.set_colorkey((154, 102, 19))
    cat_back_card = pygame.transform.scale(cat_back_card, (CARD_WIDTH, CARD_HEIGHT))
    #global back_card_rect
    #back_card_rect= cat_back_card.get_rect(topleft=(400, 200))
    screen.blit(cat_back_card, (400, 200))
    cat_used_cards = pygame.image.load(CAT[used_cards[-1]])
    cat_used_cards.set_colorkey((154, 102, 19))
    cat_used_cards = pygame.transform.scale(cat_used_cards, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(cat_used_cards, (1000, 200))

    card_rects = []
    #if show_new_card:
        #chosen_number = random.choice(numbers)
        #numbers.remove(chosen_number)
        #new_card = pygame.image.load(CAT[chosen_number])
    # new_card.set_colorkey((154, 102, 19))
    # new_card = pygame.transform.scale(cat_back_card, (CARD_WIDTH, CARD_HEIGHT))

      #screen.blit(new_card, (600, 200))
    for i in range(4):
        card_image = pygame.image.load(CAT[set_of_cards.get_cards()[i]])
        card_image.set_colorkey((154, 102, 19))
        card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
        #screen.blit(card_image, (280+200*i, 540))
        card_rect = card_image.get_rect(topleft=(280 + 200 * i, 540))
        screen.blit(card_image, card_rect)
        card_rects.append(card_rect)
    pygame.display.flip()
    return screen

def draw_the_card(screen):
    global show_new_card
    global current_card
    current_card = random.choice(numbers)
    numbers.remove(current_card)
    new_card = pygame.image.load(CAT[current_card])
    new_card.set_colorkey((154, 102, 19))
    new_card = pygame.transform.scale(new_card, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(new_card, (600, 200))
    pygame.display.flip()
    return current_card

def handle_mouse_click(event, screen):
    global show_new_card
    global current_card
    #global selected_card  # Modify the global variable
    mouse_x, mouse_y = event.pos
    if back_card_rect.collidepoint(mouse_x, mouse_y) and not show_new_card:
        show_new_card = True
        current_card = draw_the_card(screen)
    elif show_new_card:
        t=False
        for i, card_rect in enumerate(card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                t=True
                used_cards.append(set_of_cards.get_a_specific_card(i))
                set_of_cards.set_a_card(i, current_card)
                show_new_card = False
        if t:
            create_new_screen(screen)





def main():
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    screen = create_new_screen(screen)

    #used_cards = []
    #used_cards.append(23)
    #used_cards.append(43)
    #used_cards[-1]

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        my_socket.connect((IP, PORT))
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        my_socket.close()
    pygame.display.flip()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event, screen)


pygame.quit()


if __name__ == '__main__':
    main()

