def protocol_length_request_or_respond(socket, request):
    request = str(request)
    len_request = hex(len(request))
    len_request = len_request[2:]
    zfill_length = len_request.zfill(8)
    request = zfill_length + request
    socket.send(request.encode())
    print(f"sent: {request}")


def protocol_decryption_request(socket):
    length = socket.recv(8).decode()
    return socket.recv(int(length, 16)).decode()