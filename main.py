import socket
from Protocoly import *
IP = '0.0.0.0'
PORT = 1729
QUEUE_LEN = 4
four_decks=[[], [], [], []]

def get_valid_integer():
    while True:
        user_input = input("Enter an integer between 2 and 4: ")
        if user_input.isdigit():
            number = int(user_input)
            if 2 <= number <= 4:
                return number
def main():
    current_deck=-1
    number_of_players= get_valid_integer()
    client_sockets = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_LEN)
        while len(client_sockets) < number_of_players:
            client_socket, address = server_socket.accept()
            print(f"Client connected from {address}")
            client_sockets.append(client_socket)
        while True:
            for client_socket in client_sockets:
                current_deck +=1
                if current_deck == 5:
                    current_deck=0
                client_socket, client_address = server_socket.accept()
                try:
                    protocol_length_request_or_respond(client_socket, "start: player number" + str(current_deck+1))
                    while True:
                        data = protocol_decryption_request(client_socket)
                        break
                    if data!='ratatat':
                        numbers = data[0]
                        used_cards=data[1]
                        four_decks[current_deck] = data[2]
                        client_socket.sendall(data)
                except socket.error as err:
                    print(f"Received socket error on client socket: {err}")
                    client_socket.close()
    except socket.error as err:
        print(f"Received socket error on server socket: {err}")
    finally:
        for client_socket in client_sockets:
            client_socket.close()
        server_socket.close()

if __name__ == '__main__':
    main()
