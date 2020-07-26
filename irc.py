import socket
import time

class Client:
    """Class IRC client"""
    def __init__(self, addr=str, port=int, nickname="Guest", fullname="John Doe", password=""):
        """Constructor. Setup the socket."""
        self.addr = addr
        self.port = port
        self.nickname = nickname
        self.fullname = fullname
        self.password = password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.logged = False

    def connect(self):
        """Connect the user into the IRC server"""
        self.socket.connect((self.addr, self.port))
        self.connected = True
        print("Connected to " + self.addr + ":{}".format(self.port))

    def login(self):
        self.sendCommand("NICK " + self.nickname)
        self.sendCommand("USER " + self.nickname + " "  + self.nickname + " " + self.nickname + " :" + self.fullname)
        if self.password != "":
            self.sendCommand("PASS " + self.password)
        self.logged = True

    def getResponse(self):
        return self.socket.recv(4096)

    def disconnect(self):
        """Disconnect the user from the IRC server"""
        print("Disconnecting from the server...")
        self.sendCommand("QUIT :Bye")
        self.connected = False

    def sendTo(self, user, text):
        self.sendCommand("PRIVMSG " + user + ":" + text)

    def join(self, channel):
        self.sendCommand("JOIN " + channel)

    def sendCommand(self, cmd=str):
        self.socket.send((cmd + "\r\n").encode())
        data = self.getResponse()
        print(data.decode())
        return data.decode()

    def pingHandler(self):
        data = self.getResponse()
        if data.find(b"PING") != -1:
            pong = data.decode().split(':')[1]
            self.socket.send(pong.encode())
            return "PING"
        else:
            return data.decode()

    def __del__(self):
        if self.socket is not None:
            self.socket.close()