import socketserver, threading

storage = {}


class ThreadedTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        data += ' currently on thread: ' + str(threading.current_thread())
        # storage[threading.current_thread()] = str(data)
        # print(self.client_address[0] + ' wrote: ' + str(data))
        #
        # if all(storage) == threading.current_thread():
        #     pass
        # else:
        #     for thread in storage:
        #         if thread != threading.current_thread():
        self.request.sendall(bytes(data, 'ascii'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


HOST, PORT = 'localhost', 9999

server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)

server_thread = threading.Thread(target=server.serve_forever())

server_thread.daemon = True
server_thread.start()

print('Server loop in thread: ' + server_thread.name)
