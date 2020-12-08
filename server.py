import socket, sys

# see os.path

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)

while True:
    client_socket, client_address = server.accept()
    recvdata = ''.encode('UTF-8')
    while True:
        recvdata += client_socket.recv(4096)
        if "\r\n\r\n".encode('UTF-8') in recvdata:
            break
    print('Received: ', recvdata)
    dataArray = recvdata.decode().split("\r\n")
    ask = dataArray[0]
    connection = dataArray[2].split(" ")[1]
    path = ask.split(" ")[1]
    if path == "/":
        msg = "HTTP/1.1 200 OK\r\n Connection: keep-alive\r\n Content-Length: 11\r\n\r\n".encode('UTF-8')
        msg = msg + open("files/index.html", "rb").read()
        client_socket.send(msg)
    elif ".ico" in path:
        msg = "HTTP/1.1 200 OK\r\n Connection: keep-alive\r\n Content-Length: 11\r\n\r\n".encode('UTF-8')
        msg = msg + open("files" + path, "rb").read()
        client_socket.send(msg)
        # ico
    elif ".jpg" in path:
        pass
        # jpg
    elif path == "/redirect":
        # send result.html
        pass
    else:
        # all other files
        pass
    if connection == "keep-alive":
        pass
    elif connection == "close":
        client_socket.close()
        print('Client disconnected')
