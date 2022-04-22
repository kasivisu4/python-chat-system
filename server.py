#Server Program
from threading import Thread
import socket

        


class ServerThread(Thread):
    def __init__(self, mySocket,ip_connected,user_id):
        Thread.__init__(self)
        self.mySocket = mySocket
        self.mySocket.send(bytes("Welcome TO Manish Chat Server System", 'utf-8'))
        self.ip_connected = ip_connected
        self.user_id = user_id
    def run(self):
        # write code to receive data continuously
        while True:
            msg = self.mySocket.recv(1024)
            msg = msg.decode('utf-8')
            commands_supported = {
            "/help                 ": "All the supported commands of chat system",
            "/users                " : "To List All Users Connected to chat system",
            "/dm username \"message\"" : "send the message to the specified user",
            "/bc \"message\"         " : "Broadcast the message to all the users connected to chat system",
            "/quit                 " : "Disconnect from server"
            }

            if msg.startswith('/users'):
                self.mySocket.send(bytes(str(self.ip_connected.keys())[11:-2].replace('\'',''), 'utf-8'))
            elif msg.startswith('/dm'):
                msg_cmd = msg.split(' ')
               
                if len(msg_cmd) !=3:
                    self.mySocket.send(bytes("Please check the following command arguments and pass correctly", 'utf-8'))
                    self.mySocket.send(bytes("List Of Commands Accepted by Server:\n "+str(commands_supported)[1:-1].replace(",","\n").replace('\'',''), 'utf-8'))
                    continue
                if msg_cmd[2][0]!="\"" or msg_cmd[2][-1]!="\"":
                    self.mySocket.send(bytes("Please send the message in double quotes...", 'utf-8'))
                    continue
                if msg_cmd[1] not in ip_connected:
                    self.mySocket.send(bytes("User does't exist...", 'utf-8'))
                    continue

                ip_connected[msg_cmd[1]]["socket"].send(bytes(msg_cmd[2][1:-1], 'utf-8'))
            elif msg.startswith('/bc'):
                msg_cmd = msg.split(' ')
                if len(msg_cmd) !=2:
                    self.mySocket.send(bytes("Please check the following command arguments and pass correctly", 'utf-8'))
                    self.mySocket.send(bytes("List Of Commands Accepted by Server:\n "+str(commands_supported)[1:-1].replace(",","\n").replace('\'',''), 'utf-8'))
                    continue
                if msg_cmd[1][0]!="\"" or msg_cmd[1][-1]!="\"":
                    self.mySocket.send(bytes("Please send the message in double quotes...", 'utf-8'))
                    continue
                for user in ip_connected.values():
                    user["socket"].send(bytes(msg_cmd[1][1:-1], 'utf-8'))
            elif msg.startswith('/quit'):
                self.ip_connected.pop(self.user_id, None)
            else:
                self.mySocket.send(bytes("List Of Commands Accepted by Server:\n "+str(commands_supported)[1:-1].replace(",","\n").replace('\'',''), 'utf-8'))
                

# create a socket object
s = socket.socket(
    socket.AF_INET, # internet address family => IP v4
    socket.SOCK_STREAM # TCP
)
# bind socket with a port number
s.bind(('127.0.0.1', 2011))

ip_connected = {}
counter = 0
while True:
# keep System_1 in listening mode
    s.listen()
    # accept the incoming connection request
    mySocket, address = s.accept()
    if(address[0]+str(address[1]) not in ip_connected):
        counter+=1
        ip_connected["User_"+str(counter)]={"addr":address[0]+str(address[1]),"socket":mySocket}


    # create a thread to send data
    serverThread = ServerThread(mySocket,ip_connected, "User_"+str(counter))
    serverThread.start()