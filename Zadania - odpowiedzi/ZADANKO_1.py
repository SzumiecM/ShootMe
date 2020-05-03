import socket
from _thread import *

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server Started")

players = [400, 600]

strPlayers = str(players[0]) + ',' + str(players[1])


def threaded_client(conn, player):
    conn.sendall(str.encode(strPlayers + ',' + str(player)))
    reply = ""
    while True:
        try:
            info = conn.recv(2048).decode()

            players[player] = int(info)

            if not info:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = str(players[0])
                else:
                    reply = str(players[1])

                print("Received: ", info)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))

        except:
            break
        print(players)
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
