import socket
import pygame
import pickle
import random
import time
import select
from Protocoly import *
from SetOfCards import SetOfCards


IP = '127.0.0.1'
PORT = 1729
WINDOW_WIDTH = 1373
WINDOW_HEIGHT = 810
WHITE = (255, 255, 255)
COLOR_KEY = 154, 102, 19
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
BACKGROUND = 'CatBackground.jpg'
CAT = ["Cat0.png", "Cat1.png", "Cat2.png", "Cat3.png", "Cat4.png", "Cat5.png", "Cat6.png", "Cat7.png", "Cat8.png", "Cat9.png", "CatPeek.png", "CatDraw2.png", "CatBlank.png"]
CARD_WIDTH = 181
CARD_HEIGHT = 240
CAT12= 'CatBackCard.png'
BOUNDARY_THICKNESS = 8
PLACEMENT_USED_CARDS= (1000, 200)
PLACEMENT_NEW_CARD = (600, 200)
PLACEMENT_BACK_CARD = (400, 200)
PLACEMENT_START_OF_SCREEN = (0, 0)
ZERO = 0
ONE = 1
THREE = 3
ELEVEN = 11
used_cards = [12]
back_card_rect=pygame.Rect(400, 200, CARD_WIDTH, CARD_HEIGHT)
cat_used_cards_rect = pygame.Rect(1000, 200, CARD_WIDTH, CARD_HEIGHT)
card_rects = []
#card_rects = [(280, 540, 181, 240), (480, 540, 181, 240), (680, 540, 181, 240), (880, 540, 181, 240)]
#card_rects = [<rect(280, 540, 181, 240)>, <rect(480, 540, 181, 240)>, <rect(680, 540, 181, 240)>, <rect(880, 540, 181, 240)>, <rect(280, 540, 181, 240)>, <rect(480, 540, 181, 240)>, <rect(680, 540, 181, 240)>, <rect(880, 540, 181, 240)>]
current_card = ZERO
show_new_card = False
#the amount of every card in the stack

numbers = []
set_of_cards: SetOfCards
'''
numbers = [i for i in range(7)] * 4 + [7, 8] * 5 + [9] * 7 + [10, 10, 10, 11, 11, 11]
selected_numbers = random.sample(numbers, 4)
set_of_cards = SetOfCards(selected_numbers)
for number in selected_numbers:
    numbers.remove(number)
'''
#font = pygame.font.SysFont(None, 36)

def display_message(screen, message):
    try:
        font1 = pygame.font.SysFont("Arial", 45, bold=False, italic=False)
        text_surface =font1.render(message, True, BLACK_COLOR)
        screen.blit(text_surface, (450, 100))
        pygame.display.flip()
    except pygame.error as e:
        print("Error rendering text:", e)
'''
def display_message(screen, message):
    font = pygame.font.SysFont(None, 36)
    text_surface =font.render(message, True, BLACK_COLOR)
    text_rect = text_surface.get_rect(center=(500, 200))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
'''

def create_new_screen(screen, is_your_turn):
    global card_rects
    pygame.display.set_caption("RatATat")
    background = pygame.image.load(BACKGROUND)
    screen.blit(background, PLACEMENT_START_OF_SCREEN)
    #pygame.display.flip()
    if is_your_turn:
        pygame.draw.rect(screen, GREEN_COLOR, (0, 0, WINDOW_WIDTH, BOUNDARY_THICKNESS))  # Top boundary
        pygame.draw.rect(screen, GREEN_COLOR, (0, 0, BOUNDARY_THICKNESS, WINDOW_HEIGHT))  # Left boundary
        pygame.draw.rect(screen, GREEN_COLOR,(0, WINDOW_HEIGHT - BOUNDARY_THICKNESS, WINDOW_WIDTH, BOUNDARY_THICKNESS))  # Bottom boundary
        pygame.draw.rect(screen, GREEN_COLOR,(WINDOW_WIDTH - BOUNDARY_THICKNESS, 0, BOUNDARY_THICKNESS, WINDOW_HEIGHT))  # Right boundary

    cat_back_card = pygame.image.load(CAT12)
    cat_back_card.set_colorkey(COLOR_KEY)
    cat_back_card = pygame.transform.scale(cat_back_card, (CARD_WIDTH, CARD_HEIGHT))
    #global back_card_rect
    #back_card_rect= cat_back_card.get_rect(topleft=(400, 200))
    screen.blit(cat_back_card, PLACEMENT_BACK_CARD)
    cat_used_cards = pygame.image.load(CAT[used_cards[-1]])
    cat_used_cards.set_colorkey(COLOR_KEY)
    cat_used_cards = pygame.transform.scale(cat_used_cards, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(cat_used_cards, PLACEMENT_USED_CARDS)

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
        card_image.set_colorkey(COLOR_KEY)
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
    new_card.set_colorkey(COLOR_KEY)
    new_card = pygame.transform.scale(new_card, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(new_card, PLACEMENT_NEW_CARD)
    pygame.display.flip()
    return current_card


def handle_mouse_click(event, screen):
    global show_new_card
    global current_card
    #global selected_card  # Modify the global variable
    mouse_x, mouse_y = event.pos
    if back_card_rect.collidepoint(mouse_x, mouse_y) and not show_new_card:
        show_new_card = True
        create_new_screen(screen, True)
        current_card = draw_the_card(screen)
        if current_card== ELEVEN:
            used_cards.append(current_card)
            time.sleep(0.5)
            create_new_screen(screen, True)
            current_card = draw_the_card(screen)
            show_new_card = False
            return True
    if cat_used_cards_rect.collidepoint(mouse_x, mouse_y) and not show_new_card and not len(used_cards) == ONE:
        print(3)
        pygame.draw.rect(screen, GREEN_COLOR, cat_used_cards_rect, THREE)
        pygame.display.flip()
    if show_new_card:
        t=False
        for i, card_rect in enumerate(card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                t=True
                used_cards.append(set_of_cards.get_a_specific_card(i))
                set_of_cards.set_a_card(i, current_card)
                show_new_card = False
        if cat_used_cards_rect.collidepoint(mouse_x, mouse_y):
            used_cards.append(current_card)
            show_new_card = False
            t = True
        if t:
            create_new_screen(screen, True)
    if screen.get_at(PLACEMENT_USED_CARDS) == GREEN_COLOR:
        print(5)
        for i, card_rect in enumerate(card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                removed_value = used_cards.pop()
                used_cards.append(set_of_cards.get_a_specific_card(i))
                set_of_cards.set_a_card(i, removed_value)
                create_new_screen(screen, True)

    return False


def draw_two_case(screen, event, count):
    global current_card
    global used_cards
    mouse_x, mouse_y = event.pos
    for i, card_rect in enumerate(card_rects):
        if card_rect.collidepoint(mouse_x, mouse_y):
            used_cards.append(set_of_cards.get_a_specific_card(i))
            set_of_cards.set_a_card(i, current_card)
            create_new_screen(screen, True)
            if count == ZERO:
                print(1)
                current_card = draw_the_card(screen)
            return ONE
    if cat_used_cards_rect.collidepoint(mouse_x, mouse_y):
        used_cards.append(current_card)
        create_new_screen(screen, True)
        if count == ZERO:
            print(123)
            current_card = draw_the_card(screen)
        return ONE
    return ZERO










def main():
    pygame.init()
    pygame.font.init()


    global numbers
    global used_cards
    global set_of_cards
    #all_info = [numbers, used_cards, set_of_cards]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    finish_his_turn=False
    try:
        client_socket.connect((IP, PORT))

        first_msg = protocol_decryption_request(client_socket)
        print(first_msg)
        numbers = first_msg[1]
        used_cards = first_msg[2]
        set_of_cards = first_msg[3]

        count_for_draw_two=ZERO
        is_it_draw_two = False
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = pygame.display.set_mode(size)
        screen = create_new_screen(screen, False)
        #display_message(screen, first_msg[0])
        #used_cards = []
        #used_cards.append(23)
        #used_cards.append(43)
        #used_cards[-1]
        my_turn=False
            #print screen (with new updates or no updates
        pygame.display.flip()
        finish = False
        response = ""
        while not finish:
            while not my_turn:
                rlist, _, _ = select.select([client_socket], [], [], 0)
                response = ''
                if rlist:
                    print("not empty")
                    sock = rlist[ZERO]
                    response = protocol_decryption_request(sock)
                    print(response)
                    screen = create_new_screen(screen, False)
                    if str(response[0]).startswith("It's"):
                        print(10)
                        numbers = response[ONE]
                        used_cards = response[2]
                        set_of_cards = response[3]
                        screen = create_new_screen(screen, True)
                        display_message(screen, response[0])
                        #display_message(screen, response[0])
                        my_turn = True
                    elif response[0] == 'ratatat':
                        finish = True
                        break
                    else:
                        numbers = response[0]
                        used_cards = response[1]
                        #set_of_cards = response[2]
                        screen = create_new_screen(screen, False)
                        print(set_of_cards)
                if not my_turn and not is_it_draw_two:
                    screen = create_new_screen(screen, False)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finish = True
                        break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    top_length = len(used_cards)
                    top_card = used_cards[-1]
                    if is_it_draw_two:
                        print(5)
                        print(count_for_draw_two)
                        count_for_draw_two += draw_two_case(screen, event, count_for_draw_two)
                    else:
                        is_it_draw_two = handle_mouse_click(event, screen)
                        if not is_it_draw_two and (top_length != len(used_cards) or top_card != used_cards[-1]):
                            msg = [numbers, used_cards, set_of_cards]
                            msg = pickle.dumps(msg)
                            my_turn = False
                            finish_his_turn = False
                            protocol_length_request_or_respond(client_socket, msg)
                        else:
                            finish_his_turn = True

                    if count_for_draw_two==2:
                        #draw_two_case(screen, event, count_for_draw_two)
                        count_for_draw_two=ZERO
                        is_it_draw_two = False
                        my_turn=False
                        msg = [numbers, used_cards, set_of_cards]
                        msg = pickle.dumps(msg)
                        protocol_length_request_or_respond(client_socket, msg)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not is_it_draw_two:
                        msg = ["ratatat"]
                        msg = pickle.dumps(msg)
                        my_turn = False
                        protocol_length_request_or_respond(client_socket, msg)
    except socket.error as err:
        print('received socket error ' + str(err))


pygame.quit()


if __name__ == '__main__':
    main()