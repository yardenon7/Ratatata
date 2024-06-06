"""
author: Jorden Hadas
Date: 06/06/2024
Description: The client. The final project for 11th grade. The game which I won't say the name of because im getting
tired of the pep 8 not considering it a real name
"""

import socket
import pygame
import random
import time
import select
from Protocoly import *
from SetOfCards import SetOfCards

RATATAT = 'ratatat'
IP = '127.0.0.1'
PORT = 1729
WINDOW_WIDTH = 1373
WINDOW_HEIGHT = 810
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WHITE = (255, 255, 255)
COLOR_KEY = 154, 102, 19
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
BACKGROUND = 'CatBackground.jpg'
CAT = ["Cat0.png", "Cat1.png", "Cat2.png", "Cat3.png", "Cat4.png", "Cat5.png", "Cat6.png", "Cat7.png", "Cat8.png",
       "Cat9.png", "CatPeek.png", "CatDraw2.png", "CatBlank.png"]
CARD_WIDTH = 181
CARD_HEIGHT = 240
CAT12 = 'CatBackCard.png'
BOUNDARY_THICKNESS = 8
PLACEMENT_USED_CARDS = (1000, 200)
PLACEMENT_NEW_CARD = (600, 200)
PLACEMENT_BACK_CARD = (400, 200)
PLACEMENT_START_OF_SCREEN = (0, 0)
PLACEMENT_FOR_THE_FONT = (450, 100)
THE_WAIT_TIME_FOR_DRAW_TWO = 0.5
RATATAT_ERROR = "RatATat_ERROR"
MESSAGE_ERROR = "an Error has occurred, please rerun the game"
TIME_TO_SLEEP_ERROR = 7
ZERO = 0
ONE = 1
TW0 = 2
THREE = 3
ELEVEN = 11

used_cards = [12]
back_card_rect = pygame.Rect(400, 200, CARD_WIDTH, CARD_HEIGHT)
cat_used_cards_rect = pygame.Rect(1000, 200, CARD_WIDTH, CARD_HEIGHT)
card_rects = []
current_card = ZERO
show_new_card = False
numbers = []
set_of_cards: SetOfCards


def display_message(screen, message):
    """
    :param screen: the screen
    :param message: the message the server passed (It's your turn)
    """
    try:
        font1 = pygame.font.SysFont("Arial", 45, bold=False, italic=False)
        text_surface = font1.render(message, True, BLACK_COLOR)
        screen.blit(text_surface, PLACEMENT_FOR_THE_FONT)
        pygame.display.flip()
    except pygame.error as e:
        print("Error rendering text:", e)


def create_new_screen(screen, is_your_turn):
    """
    :param screen: the screen. is_your_turn: a boolean variable that determine whether it's the client turn or not
    :param is_your_turn: a boolean variable that determine whether it's the client turn or not
    :return: the screen. If it's the client turn returns the screen with that message on it
    """
    global card_rects
    pygame.display.set_caption("RatATat")
    background = pygame.image.load(BACKGROUND)
    screen.blit(background, PLACEMENT_START_OF_SCREEN)

    if is_your_turn:
        pygame.draw.rect(screen, GREEN_COLOR, (ZERO, ZERO, WINDOW_WIDTH, BOUNDARY_THICKNESS))  # Top boundary
        pygame.draw.rect(screen, GREEN_COLOR, (ZERO, ZERO, BOUNDARY_THICKNESS, WINDOW_HEIGHT))  # Left boundary
        pygame.draw.rect(screen, GREEN_COLOR, (
            ZERO, WINDOW_HEIGHT - BOUNDARY_THICKNESS, WINDOW_WIDTH, BOUNDARY_THICKNESS))  # Bottom boundary
        pygame.draw.rect(screen, GREEN_COLOR,
                         (WINDOW_WIDTH - BOUNDARY_THICKNESS, ZERO, BOUNDARY_THICKNESS, WINDOW_HEIGHT))  # Right boundary

    cat_back_card = pygame.image.load(CAT12)
    cat_back_card.set_colorkey(COLOR_KEY)
    cat_back_card = pygame.transform.scale(cat_back_card, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(cat_back_card, PLACEMENT_BACK_CARD)

    cat_used_cards = pygame.image.load(CAT[used_cards[-1]])
    cat_used_cards.set_colorkey(COLOR_KEY)
    cat_used_cards = pygame.transform.scale(cat_used_cards, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(cat_used_cards, PLACEMENT_USED_CARDS)

    card_rects = []

    for i in range(4):
        card_image = pygame.image.load(CAT[set_of_cards.get_cards()[i]])
        card_image.set_colorkey(COLOR_KEY)
        card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
        # screen.blit(card_image, (280+200*i, 540))
        card_rect = card_image.get_rect(topleft=(280 + 200 * i, 540))
        screen.blit(card_image, card_rect)
        card_rects.append(card_rect)
    pygame.display.flip()

    return screen


def draw_the_card(screen):
    """
    :param screen: the screen.
    :return: the screen with the new card printed on it
    """
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
    """
    :param event: the event
    :param screen: the screen
    :return: True if the new card is draw_two and False otherwise. The function takes care of the clicking action the client did on the screen
    """
    global numbers
    global used_cards
    global show_new_card
    global current_card
    # global selected_card  # Modify the global variable
    mouse_x, mouse_y = event.pos

    if back_card_rect.collidepoint(mouse_x, mouse_y) and not show_new_card:
        show_new_card = True

        if len(numbers) ==0:
            first_value = used_cards.pop(0)
            numbers = used_cards.copy()
            used_cards = [first_value]

        create_new_screen(screen, True)
        current_card = draw_the_card(screen)

        if current_card == ELEVEN:
            used_cards.append(current_card)
            time.sleep(THE_WAIT_TIME_FOR_DRAW_TWO)
            create_new_screen(screen, True)

            if len(numbers) == 0:
                first_value = used_cards.pop(0)
                numbers = used_cards.copy()
                used_cards = [first_value]

            current_card = draw_the_card(screen)
            show_new_card = False
            return True

    if cat_used_cards_rect.collidepoint(mouse_x, mouse_y) and not show_new_card and not len(used_cards) == ONE:
        pygame.draw.rect(screen, GREEN_COLOR, cat_used_cards_rect, THREE)
        pygame.display.flip()

    if show_new_card:
        no_longer_new_card = False
        for i, card_rect in enumerate(card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                no_longer_new_card = True
                used_cards.append(set_of_cards.get_a_specific_card(i))
                set_of_cards.set_a_card(i, current_card)
                show_new_card = False

        if cat_used_cards_rect.collidepoint(mouse_x, mouse_y):
            used_cards.append(current_card)
            show_new_card = False
            no_longer_new_card = True

        if no_longer_new_card:
            create_new_screen(screen, True)

    if screen.get_at(PLACEMENT_USED_CARDS) == GREEN_COLOR:
        for i, card_rect in enumerate(card_rects):
            if card_rect.collidepoint(mouse_x, mouse_y):
                removed_value = used_cards.pop()
                used_cards.append(set_of_cards.get_a_specific_card(i))
                set_of_cards.set_a_card(i, removed_value)
                create_new_screen(screen, True)

    return False


def draw_two_case(screen, event, count):
    """
    :params screen: the screen. event: the event. count: the amount of times the player clicked on the packet
    returns: one if the player made a difference in the screen and 0 otherwise
    """
    global numbers
    global current_card
    global used_cards
    mouse_x, mouse_y = event.pos
    for i, card_rect in enumerate(card_rects):
        if card_rect.collidepoint(mouse_x, mouse_y):
            used_cards.append(set_of_cards.get_a_specific_card(i))
            set_of_cards.set_a_card(i, current_card)
            create_new_screen(screen, True)

            if count == ZERO:
                if len(numbers) == 0:
                    first_value = used_cards.pop(0)
                    numbers = used_cards.copy()
                    used_cards = [first_value]
                current_card = draw_the_card(screen)
            return ONE

    if cat_used_cards_rect.collidepoint(mouse_x, mouse_y):
        used_cards.append(current_card)
        create_new_screen(screen, True)

        if count == ZERO:
            if len(numbers) == 0:
                first_value = used_cards.pop(0)
                numbers = used_cards.copy()
                used_cards = [first_value]
            current_card = draw_the_card(screen)
        return ONE

    return ZERO


def main():
    pygame.init()
    pygame.font.init()

    global numbers
    global used_cards
    global set_of_cards
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((IP, PORT))
        first_msg = protocol_decryption_request(client_socket)
        print(first_msg)
        numbers = first_msg[1]
        used_cards = first_msg[2]
        set_of_cards = first_msg[3]

        count_for_draw_two = ZERO
        is_it_draw_two = False
        screen = pygame.display.set_mode(SIZE)
        screen = create_new_screen(screen, False)
        my_turn = False

        pygame.display.flip()
        finish = False

        while not finish:

            while not my_turn:
                rlist, _, _ = select.select([client_socket], [], [], 0)
                if rlist:
                    sock = rlist[ZERO]
                    response = protocol_decryption_request(sock)
                    print(response)
                    if str(response[0]).startswith(RATATAT):
                        display_message(screen, response[1])
                        time.sleep(5)
                    else:
                        screen = create_new_screen(screen, False)

                    if str(response[0]).startswith("It's"):
                        numbers = response[ONE]
                        used_cards = response[2]
                        set_of_cards = response[3]
                        screen = create_new_screen(screen, True)
                        display_message(screen, response[0])
                        my_turn = True

                    elif response[0] == RATATAT:
                        finish = True
                        break

                    elif str(response[0]).startswith("an error"):
                        msg = ["not important"]
                        msg = pickle.dumps(msg)
                        protocol_length_request_or_respond(client_socket, msg)

                    else:
                        numbers = response[0]
                        used_cards = response[1]
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
                        print(count_for_draw_two)
                        count_for_draw_two += draw_two_case(screen, event, count_for_draw_two)

                    else:
                        is_it_draw_two = handle_mouse_click(event, screen)
                        if not is_it_draw_two and (top_length != len(used_cards) or top_card != used_cards[-1]):
                            msg = [numbers, used_cards, set_of_cards]
                            msg = pickle.dumps(msg)
                            my_turn = False
                            protocol_length_request_or_respond(client_socket, msg)

                    if count_for_draw_two == 2:
                        count_for_draw_two = ZERO
                        is_it_draw_two = False
                        my_turn = False
                        msg = [numbers, used_cards, set_of_cards]
                        msg = pickle.dumps(msg)
                        protocol_length_request_or_respond(client_socket, msg)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not is_it_draw_two:
                        msg = [RATATAT]
                        msg = pickle.dumps(msg)
                        my_turn = False
                        protocol_length_request_or_respond(client_socket, msg)

    except socket.error as err:
        print('received socket error ' + str(err))
        error_screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(RATATAT_ERROR)
        background = pygame.image.load(BACKGROUND)
        error_screen.blit(background, PLACEMENT_START_OF_SCREEN)
        display_message(error_screen, MESSAGE_ERROR)
        pygame.display.flip()
        time.sleep(TIME_TO_SLEEP_ERROR)


pygame.quit()

if __name__ == '__main__':
    main()
