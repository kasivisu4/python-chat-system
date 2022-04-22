#Client Program

from threading import Thread
import socket
import sys

class MySendingThread(Thread):
    def __init__(self, mySocket):
        Thread.__init__(self)
        self.mySocket = mySocket

    def run(self):
        # write code to send data to System_1
        while True:
            data = input()
            self.mySocket.send(bytes(data, 'utf-8'))
            if(data == "/quit"):
                print("quitting the server")
                sys.exit()


class MyReceivingThread(Thread):
    def __init__(self, mySocket):
        Thread.__init__(self)
        self.mySocket = mySocket

    def run(self):
        # write code to receive data from System_1
        while True:
            msg = self.mySocket.recv(1024)
            print(msg.decode('utf-8'))


# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# send a connection request
server_ip = input("Please Enter the Server IP Address")
if server_ip == "":
    server_ip = "127.0.0.1"
s.connect((server_ip,2011))
# create a thread to send data => System_1
mySendThread = MySendingThread(s)
# create a thread to receive data from System_1
myReceiveThread = MyReceivingThread(s)
# start both threads
mySendThread.start()
myReceiveThread.start()