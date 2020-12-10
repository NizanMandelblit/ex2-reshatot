import socket
import sys
from os import path


def file_doesnt_exist(client_socket):
    msg = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode('UTF-8')
    client_socket.send(msg)
    #print("server send:")
    #print(msg.decode())
    client_socket.close()


TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(4)  # we can't limit the number of connections
# server.settimeout(1)  # Sets the socket to timeout after 1 second of no activity
connection = "close"

while True:
    # client_socket, client_address = server.accept()

    if connection == "close":
        client_socket, client_address = server.accept()
    client_socket.settimeout(1.0)
    recvdata = ''.encode('UTF-8')
    got_timeout = 0
    while True:
        try:
            recvdata += client_socket.recv(4096)
        except socket.timeout:
            got_timeout = 1
            break
        if "\r\n\r\n".encode('UTF-8') in recvdata:
            break
        elif recvdata.decode() == "":
            break
    client_socket.settimeout(None)
    # Got timeout
    if got_timeout == 1:
        print('Got timeout')
        client_socket.close()
        connection = "close"
        print('Client disconnected')
        continue

    # Got empty message
    if recvdata == "" or recvdata == "".encode('UTF-8'):
        print('Got empty message')
        client_socket.close()
        connection = "close"
        print('Client disconnected')
        continue

    print("client send:")
    print(recvdata.decode())
    dataArray = recvdata.decode().split("\r\n")
    ask = dataArray[0]  # "Get" string
    connection = dataArray[2].split(" ")[1]  # dataArray[2] runtime error?
    file_path = ask.split(" ")[1]
    if file_path == "/":  # index.html
        file = open("files/index.html", "rb").read()
        msg = "HTTP/1.1 200 OK\r\nConnection: ".encode('UTF-8') + connection.encode(
            'UTF-8') + "\r\nContent-Length: ".encode('UTF-8') + str(len(file)).encode('UTF-8') + "\r\n\r\n".encode(
            'UTF-8') + file
        client_socket.send(msg)
        #print("server send:")
        #print(msg.decode())
    elif file_path == "/redirect":
        # send result.html
        file = open("files/result.html", "rb").read()
        #  more new line?
        msg = "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n".encode("UTF-8")\
              + file
        client_socket.send(msg)
        #print("server send:")
        #print(msg.decode())
        client_socket.close()
        connection = "close"
        continue
    else:  # jpg,ico, all other files
        if "files" in file_path:  # can be?
            file = open(file_path[1:], "rb").read()
        else:
            is_exist = path.exists("files"+file_path)
            if not is_exist:
                file_doesnt_exist(client_socket)
                connection = "close"
                continue
            file = open("files"+file_path, "rb").read()
        msg = "HTTP/1.1 200 OK\r\nConnection: ".encode('UTF-8') + connection.encode(
            'UTF-8') + "\r\nContent-Length: ".encode('UTF-8') + str(len(file)).encode('UTF-8') + "\r\n\r\n".encode(
            'UTF-8') + file
        client_socket.send(msg)
        # print("server send:")
        # print(msg.decode())

    if connection == "keep-alive":
        continue
    elif connection == "close":
        client_socket.close()
        print('Client disconnected')



