"""
author: Jorden Hadas
Date: 06/06/2024
Description: The server. The final project for 11th grade. The game which I won't say the name of because im getting
tired of the pep 8 not considering it a real name
"""
import socket
from Protocoly import *
import pickle
import random
from SetOfCards import SetOfCards

IP = '0.0.0.0'
PORT = 1729
QUEUE_LEN = 4
THE_MIN_IN_SCALE = 2
THE_MAX_IN_SCALE = 4
THE_AMOUNT_OF_CARDS_IN_DECK = 4
WINNER_MESSAGE = "the winners are player/s number:"
THE_INPUT_MESSAGE = "Enter the number of players. The number has to be between 2 and 4: "
RATATAT = "ratatat"
AN_ERROR_MASSAGE = "an error has happened"
TIMEOUT_FOR_SOCKET = 30

four_decks = []
numbers = [i for i in range(7)] * 4 + [7, 8] * 5 + [9] * 7 + [11, 11, 11]
used_cards = [12]


def get_valid_integer():
    """
    :return: the number of players
    """
    while True:
        user_input = input(THE_INPUT_MESSAGE)
        if user_input.isdigit():
            number = int(user_input)
            if THE_MIN_IN_SCALE <= number <= THE_MAX_IN_SCALE:
                return number


def make_the_decks(number_of_players):
    """
    :param number_of_players: the number of the players
    :return: nothing. The function makes the decks
    """
    for i in range(number_of_players):
        selected_numbers = random.sample(numbers, THE_AMOUNT_OF_CARDS_IN_DECK)
        four_decks.append(SetOfCards(selected_numbers))
        for number in selected_numbers:
            numbers.remove(number)


def check_who_wins(the_decks):
    """
    :param the_decks: the decks of the game
    :return: the players who won (in a list)
    """
    min_sum = 1000  # Initialize max_sum to negative infinity
    min_sum_indices = []  # Initialize list to store indices with minimum sum

    # Iterate through each list in the list_of_lists
    for index, sublist in enumerate(the_decks):
        current_sum = sum_the_deck(sublist.get_cards())  # Calculate sum of current sublist
        if current_sum < min_sum:
            min_sum = current_sum

    for index, sublist in enumerate(the_decks):
        current_sum = sum_the_deck(sublist.get_cards())
        if current_sum == min_sum:
            min_sum_indices.append(index + 1)

    return min_sum_indices


def sum_the_deck(deck):
    """
    :param: a deck of a player
    :return: the summary of the deck
    """
    total = 0
    for item in deck:
        if item < 10:
            total += item
        else:
            total += 10
    return total


def main():
    global numbers
    global used_cards
    end_of_game = False
    current_deck = 1
    number_of_players = get_valid_integer()
    client_sockets = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    make_the_decks(number_of_players)
    print(four_decks)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_LEN)
        print(number_of_players)
        while len(client_sockets) < number_of_players:
            print(number_of_players)
            print(client_sockets)
            client_socket, address = server_socket.accept()
            print(f"Client connected from {address}")
            client_sockets.append(client_socket)
            print(current_deck)
            first_msg = [f"You are player number: {str(current_deck)}", numbers, used_cards,
                         four_decks[current_deck - 1]]
            first_msg = pickle.dumps(first_msg)
            protocol_length_request_or_respond(client_socket, first_msg)
            current_deck += 1
        current_deck = -1
        try:
            while True:
                for client_socket in client_sockets:
                    current_deck += 1
                    if current_deck == number_of_players:
                        current_deck = 0
                    the_data_to_send = [f"It's your turn, player number: {str(current_deck + 1)}", numbers, used_cards,
                                        four_decks[current_deck]]
                    the_data_to_send = pickle.dumps(the_data_to_send)
                    protocol_length_request_or_respond(client_socket, the_data_to_send)
                    while True:
                        client_socket.settimeout(TIMEOUT_FOR_SOCKET)
                        data = protocol_decryption_request(client_socket)
                        break
                    if not data:
                        protocol_length_request_or_respond(client_socket, 5)
                    if data[0] != RATATAT:
                        numbers = data[0]
                        used_cards = data[1]
                        four_decks[current_deck] = data[2]
                        the_data = [numbers, used_cards, four_decks[current_deck]]
                        the_data = pickle.dumps(the_data)
                        for client_socket1 in client_sockets:
                            protocol_length_request_or_respond(client_socket1, the_data)
                    else:
                        end_of_game = True
                        break
                if end_of_game:
                    break
            the_winners = check_who_wins(four_decks)
            the_data = [RATATAT, WINNER_MESSAGE + str(the_winners)]
            the_data = pickle.dumps(the_data)
            for client_socket1 in client_sockets:
                protocol_length_request_or_respond(client_socket1, the_data)
        except socket.error as err:
            print(err)
            for client_socket in client_sockets:
                try:
                    the_data = [AN_ERROR_MASSAGE]
                    the_data = pickle.dumps(the_data)
                    protocol_length_request_or_respond(client_socket, the_data)
                except socket.error as er:
                    print(er)
    except socket.error as err:
        print(f"Received socket error on server socket: {err}")
    finally:
        for client_socket in client_sockets:
            client_socket.close()
        server_socket.close()


if __name__ == '__main__':
    main()
