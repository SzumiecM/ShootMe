import socketserver

storage = {}


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]) + '   ' + str(socket))
        print(data)
        socket.sendto(data.upper(), self.client_address)


HOST, PORT = "localhost", 9999
server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
server.serve_forever()
