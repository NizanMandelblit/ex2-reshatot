import socket, sys

# see os.path

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(1)
# server.settimeout(1)  # Sets the socket to timeout after 1 second of no activity

while True:
    client_socket, client_address = server.accept()
    recvdata = ''.encode('UTF-8')
    while True:
        recvdata += client_socket.recv(4096)
        if "\r\n\r\n".encode('UTF-8') in recvdata:
            break
        elif recvdata == "":
            break
    print(recvdata.decode())
    dataArray = recvdata.decode().split("\r\n")
    ask = dataArray[0]
    connection = dataArray[2].split(" ")[1]
    path = ask.split(" ")[1]
    if path == "/":  # index.html
        msg = open("files/index.html", "rb").read()
        msg = "HTTP/1.1 200 OK\r\n Connection: ".encode('UTF-8') + connection.encode(
            'UTF-8') + "\r\n Content-Length: ".encode('UTF-8') + str(len(msg)).encode('UTF-8') + "\r\n\r\n".encode(
            'UTF-8') + msg
        client_socket.send(msg)
    elif ".jpg" in path or ".ico" in path:  # jpg,ico
        if "files" in path:
            msg = open(path[1:], "rb").read()
        else:
            msg = open("files"+path, "rb").read()
        msg = "HTTP/1.1 200 OK\r\n Connection: ".encode('UTF-8') + connection.encode(
            'UTF-8') + "\r\n Content-Length: ".encode('UTF-8') + str(len(msg)).encode('UTF-8') + "\r\n\r\n".encode(
            'UTF-8') + msg
        client_socket.send(msg)
    elif path == "/redirect":
        # send result.html
        msg = open("files/result.html", "rb").read()
        msg="HTTP / 1.1 301 Moved Permanently\r\n Connection: close\r\n Location: / result.html\r\n \r\n\r\n".encode("UTF-8")+msg
        client_socket.send(msg)
        client_socket.close()
        continue
    else:
        # all other files
        pass
    if connection == "keep-alive":
        pass
    elif connection == "close":
        client_socket.close()
        print('Client disconnected')
