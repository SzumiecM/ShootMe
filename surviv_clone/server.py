import socket
from _thread import *
from Gameplay import Gameplay
import pickle
import pygame

pygame.init()

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

g = Gameplay()
playerindexes = []
base = []
for i in range(g.max_players):
    playerindexes.append(i)
    base.append([g.allPlayersToPickle[i], [], []])

print(base)


def threaded_client(conn, player):
    conn.send(pickle.dumps([base, player, g.boxes]))
    reply = ""
    while True:
        try:
            playerData = pickle.loads(conn.recv(8192))  # pobieramy tylko playera
            base[player] = playerData

            if not playerData:
                print("Disconnected")
                break
            else:
                # if player == 1:
                #     reply = base[0]
                # else:
                #     reply = base[1]

                reply = []

                for user in base:
                    if base.index(user) == player:
                        reply.append('')
                    else:
                        reply.append(user)

                print("Received: ", playerData)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))  # wysyłamy wszystkich graczy oprócz playera
        except:
            break

    print("Lost connection")
    conn.close()
    base[player][0]['weapon'] = 'hand'
    playerindexes.insert(0, player)


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, playerindexes.pop(0)))
