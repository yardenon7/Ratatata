import socket

IP = '0.0.0.0'
PORT = 1729
QUEUE_LEN = 4

def main():
    client_sockets = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_LEN)
        while True:
            if len(client_sockets) < 2:
                client_socket, address = server_socket.accept()
                print(f"Client connected from {address}")
                client_sockets.append(client_socket)
            if len(client_sockets) == 2:
                break
        while True:
            for i in range(2):
                client_socket = client_sockets[i]
            except socket.error as err:
                print('received socket error on client socket' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        print('received socket error on server socket' + str(err))
    finally:
        server_socket.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
