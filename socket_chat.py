import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("10.1.20.101", 50000))
s.listen(1)

clients = {}

class client(threading.Thread):
    nickname = False

    def __init__(self, addr, socket):
        threading.Thread.__init__(self)
        self.addr = addr
        self.socket = socket

    def send(self, message):
        self.socket.send(message.encode())

    def sendAll(self, message):
        print("[{}] {}".format(self.addr, message))
        if(self.nickname==False):
            name = self.addr
        else:
            name = self.nickname
        for client in clients.items():
            if str(client.socket) != str(self.socket):
                client.send(("[{}] {}".format(name, message)))

    def sendSelf(self, message):
        self.socket.send(message.encode())

    #define command functionality
    def helpText(self):
        self.sendSelf('commands: /nick')
    def nick(self, parts):
        name = parts[1]
        self.nickname = name
    def execute_command(self, parts):
        switcher = {
            '/help': self.helpText,
            '/nick': self.nick
        }
        return switcher.get(parts[0], self.helpText)()
    def run(self):
        while True: 
            data = self.socket.recv(1024)
            if not data.decode().startswith("/"):
                self.sendAll(data.decode())
            else:
                command_parts = data.decode().split(' ')
                self.execute_command(command_parts)




try:
    while(True):
        komm, addr = s.accept()
        clientId = str(addr)
        newClient = client(clientId, komm)
        newClient.start()
        clients[clientId] = newClient
        print('Neuer Client verbunden. IP: '+clientId)
finally:
    s.close()
