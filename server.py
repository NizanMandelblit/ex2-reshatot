import socket,sys


# see os.path

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(5)

while True:
    client_socket, client_address = server.accept()
    data = client_socket.recv(100)
    print('Received: ', data)
    dataArray = data.decode().split("\r\n")
    ask = dataArray[0]
    path = ask.split(" ")[1]
    if path == "/":
        f = open("files/index.html", "r")
        lines = f.readlines()
        while f.readline():
            client_socket.send(str(f.readlines()).encode())
    elif path == "":
        pass
        # jpg, ico
    elif path == "/redirect":
        # send result.html
        pass
    else:
        # all other files
        pass
    client_socket.close()
    print('Client disconnected')
