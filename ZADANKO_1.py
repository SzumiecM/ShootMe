import socket
from _thread import *

server = "localhost"
port = 5555

#TODO stwórz socket operujący na ipv4 i protokole TCP
# s = socket.socket(WSTAW ODPOWIEDNIE ARGUMENTY)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    #TODO przypisz socketowi s odpowiedni adres i port (zdefiniowane u góry) funkcją
    # s.bind()
    s.bind((server, port))
except socket.error as e:
    str(e)

#TODO ustaw socket w tryb nasłuchiwania
s.listen()
print("Waiting for a connection, Server Started")

#TODO stwórz dwuelementową listę players i wpisz do niej dwie liczby
# pierwsza będzie zwiększana do 1000 przez pierwszego klienta, a druga zmniejszana do 0 przez drugiego
players = [400, 600]

strPlayers = str(players[0]) + ',' + str(players[1])

def threaded_client(conn, player):
    conn.sendall(str.encode(strPlayers + ',' + str(player)))
    reply = ""
    while True:
        try:
            info = conn.recv(2048).decode()

            #TODO zaktualizuj listę players, pamiętając że otrzymane dane opisują tylko gracza, który je wysłał
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

            #TODO zakoduj podobnie jak po wywołaniu funkcji wiadomość i wyślij ją do klienta
            conn.sendall(str.encode(reply))

        except:
            break
        print(players)
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    #TODO zaakceptuj połączenie z zewnątrz funkcją s.accept(), zwróci ona dwie wartości,
    # połączenie za pomocą którego będziemy wysyłać i odbierać dane oraz adres, zapisz te zmienne jako conn i addr
    conn, addr = s.accept()
    print("Connected to:", addr)

    #TODO rozpocznij nowy wątek przy pomocy funkncji
    # start_new_thread(<WYWOŁYWANA FUNKCJA>, <OBIEKT TUPLE ZAWIERAJĄCY POŁĄCZENIE I NUMER GRACZA (ARGUMENTY)>)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
