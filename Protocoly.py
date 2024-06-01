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