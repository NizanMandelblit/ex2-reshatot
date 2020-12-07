import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('', 12345))

server.listen(5)

while True:
    client_socket, client_address = server.accept()

    data = client_socket.recv(100)
    print('Received: ', data)
    dataArray = data.decode().split(" ")
    if dataArray[1] == "/":
        f = open("files/index.html", "r")
        while f.readline():
            client_socket.send(str(f.readlines()).encode())
    client_socket.close()
    print('Client disconnected')
