import socket, time

HOST, PORT = "localhost", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(20):
    sock.sendto(bytes(str(i) + "\n", "utf-8"), (HOST, PORT))
    received = str(sock.recv(1024), "utf-8")
    print('Sent: ' + str(i))
    print('Received: ' + received)
    time.sleep(1)
