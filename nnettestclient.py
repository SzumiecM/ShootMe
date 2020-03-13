import socket, time

HOST, PORT = 'localhost', 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = 'some input'

names = ['mike', 'john']

def send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        return response
    finally:
        pass
        #sock.close()




for i in range(20):
    print('SENT: ' + str(i))
    print('RECEIVED: ' + send(HOST, PORT, str(i)))
    time.sleep(5)



