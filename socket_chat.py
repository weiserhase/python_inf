import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.178.137", 50000))
s.listen(1)

connections = {}

class recv_thread (threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self. addr = addr
    def run(self):
        while True: 
            data = connections[self.addr].recv(1024)
            print("[{}] {}".format(self.addr, data.decode()))
            for key, value in connections.items():
                if key != str(self.addr): 
                    value.send(("[{}] {}".format(self.addr, data.decode())).encode())

try:
    while(True):
        print('in while')
        komm, addr = s.accept()
        clientIp = addr[0]
        connections[clientIp] = komm
        print('before thread init')
        newT = recv_thread(clientIp)
        print('before thread start')
        newT.start()
        print('after thread start')
finally:
    s.close()
