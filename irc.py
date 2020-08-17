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

    def ask_config(self):
        """Ask the mandatory options to the user"""
        self.addr = input("Ip address: ")

        next_step = False
        while next_step is False:
            tmp = input("Port (6667): ")
            if tmp == "":
                next_step = True
            elif type(tmp) is int or (type(tmp) is str and tmp.isdigit() is True):
                self.port = int(tmp)
                next_step = True
            else:
                print("Please enter a valid port.")

        next_step = False
        while next_step is False:
            tmp = input("Nickname (\"Guest\"): ")
            if tmp == "":
                next_step = True
            elif len(tmp) <= 31:
                next_step = True
                self.nickname = tmp
            else:
                print("Invalid nickname (over 31 characters).")
        
        next_step = False
        while next_step is False:
            tmp = input("Real Name (\"John Doe\"): ")
            if tmp == "":
                next_step = True
            elif len(tmp) <= 31:
                next_step = True
                self.nickname = tmp
        
        self.password = input("Password (press enter if empty): ")


    def connect(self):
        """Connect the user into the IRC server"""
        if self.addr is None:
            print("No ip address given.")
            return
        self.socket.connect((self.addr, self.port))
        self.connected = True
        self.socket.setblocking(True)
        print("Connected to " + self.addr + ":{}".format(self.port))

    def login(self):
        self.sendCommand("NICK " + self.nickname)
        self.sendCommand("USER " + self.nickname + " "  + self.nickname + " " + self.nickname + " :" + self.fullname)
        if self.password != "":
            self.sendCommand("PASS " + self.password)
        self.logged = True

    def getResponse(self):
        return self.socket.recv(8192)

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
        """Send a command to the IRC server and wait for the response"""
        self.socket.send((cmd + "\r\n").encode())

    def pingHandler(self):
        data = self.getResponse()
        if data.find(b"PING") != -1:
            pong = data.decode().split(':')[1]
            self.socket.send(pong.encode())
            return "PING"
        else:
            return data.decode()

    def isDisconnected(self, data=bytes):
        clearedData = data.decode().split("\n")
        clearedData = clearedData[len(clearedData) - 2]
        if clearedData.startswith('ERROR :Closing link:') is True:
            self.connected = False
            return True
        else:
            return False
    def __del__(self):
        if self.socket is not None:
            self.socket.close()