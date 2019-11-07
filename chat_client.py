import socket
import threading
ip = "192.168.178.137"
port = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

def input_thread():
    while True:
        anwser = s.recv(1024)
        if not anwser:
            s.close()
            break
        print(anwser.decode())
    
t = threading.Thread(target=input_thread)
t.start()

try:
    while True:
        message = input(">> ")
        s.send(message.encode())    
finally:
    s.close()
