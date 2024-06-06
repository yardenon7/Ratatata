"""
author: Jorden Hadas
Date: 06/06/2024
Description: The protocol. The final project for 11th grade. The game which I won't say the name of because im getting
tired of the pep 8 not considering it a real name
"""
import pickle

def protocol_length_request_or_respond(socket, request):
    len_request = str(len(request))
    len_request = len_request + '!'
    request = len_request.encode() + request
    socket.send(request)


def protocol_decryption_request(socket):
    length = socket.recv(1).decode()
    while "!" not in length:
        length = length + socket.recv(1).decode()
    return pickle.loads(socket.recv((int(length[:-1]))))