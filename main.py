import socket
from Protocoly import *
import pickle
import random
from SetOfCards import SetOfCards

IP = '0.0.0.0'
PORT = 1729
QUEUE_LEN = 4
four_decks =[]
numbers = [i for i in range(7)] * 4 + [7, 8] * 5 + [9] * 7 + [10, 10, 10, 11, 11, 11, 11 ,11, 11, 11]
used_cards = [12]

def get_valid_integer():
    while True:
        user_input = input("Enter an integer between 2 and 4: ")
        if user_input.isdigit():
            number = int(user_input)
            if 2 <= number <= 4:
                return number


def make_the_decks(number_of_players):
    for i in range(number_of_players):
        selected_numbers = random.sample(numbers, 4)
        four_decks.append(SetOfCards(selected_numbers))
        for number in selected_numbers:
            numbers.remove(number)


def check_who_wins(the_decks):
    min_sum = 1000  # Initialize max_sum to negative infinity
    min_sum_indices = []  # Initialize list to store indices with minimum sum

    # Iterate through each list in the list_of_lists
    for index, sublist in enumerate(the_decks):
        current_sum = sum_the_deck(sublist.get_cards())  # Calculate sum of current sublist
        if current_sum < min_sum:
            min_sum = current_sum
            min_sum_indices = [index+1]
        elif current_sum == min_sum:
            min_sum_indices.append(index)

    return min_sum_indices


def sum_the_deck(deck):
    total = 0
    for item in deck:
        if item <10:
            total += item
        else:
            total += 10
    return total
def main():
    global numbers
    global used_cards
    end_of_game=False
    current_deck=1
    number_of_players= get_valid_integer()
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
            first_msg = [f"You are player number: {str(current_deck)}", numbers, used_cards, four_decks[current_deck-1]]
            first_msg = pickle.dumps(first_msg)
            protocol_length_request_or_respond(client_socket, first_msg)
            current_deck += 1
        print('hi')
        current_deck=-1
        while True:
            for client_socket in client_sockets:
                print(7)
                current_deck +=1
                if current_deck == number_of_players:
                    current_deck=0
                the_data_to_send = [f"It's your turn, player number: {str(current_deck + 1)}", numbers, used_cards, four_decks[current_deck]]
                the_data_to_send = pickle.dumps(the_data_to_send)
                print(the_data_to_send)
                protocol_length_request_or_respond(client_socket, the_data_to_send)
                while True:
                    data = protocol_decryption_request(client_socket)
                    break
                if data[0] != 'ratatat':
                    print(16)
                    numbers = data[0]
                    used_cards=data[1]
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
        the_data = ["ratatat", "the winners are player/s number:" + str(the_winners)]
        the_data = pickle.dumps(the_data)
        for client_socket1 in client_sockets:
            protocol_length_request_or_respond(client_socket1, the_data)
    except socket.error as err:
        print(f"Received socket error on server socket: {err}")
    finally:
        for client_socket in client_sockets:
            client_socket.close()
        server_socket.close()


if __name__ == '__main__':
    main()
