import socket
import time
import re

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

        next_step = False
        while next_step is False:
            self.addr = input("Ip address: ")
            if self.addr == "":
                print("Please write something.")
            else:
                next_step = True

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
        if self.addr is None or self.addr == "":
            print("No ip address given.")
            return
        self.socket.connect((self.addr, self.port))
        self.connected = True
        self.socket.setblocking(True)
        print("Connected to " + self.addr + ":{}".format(self.port))

    def login(self):
        self.send_command("NICK " + self.nickname)
        self.send_command("USER " + self.nickname + " "  + self.nickname + " " + self.nickname + " :" + self.fullname)
        if self.password != "":
            self.send_command("PASS " + self.password)
        self.logged = True

    def get_response(self):
        return self.socket.recv(8192)

    def disconnect(self):
        """Disconnect the user from the IRC server"""
        print("Disconnecting from the server...")
        self.send_command("QUIT :Bye")
        self.connected = False

    def send_to(self, user, text):
        self.send_command("PRIVMSG " + user + ":" + text)

    def join(self, channel):
        self.send_command("JOIN " + channel)

    def send_command(self, cmd=str):
        """Send a command to the IRC server and wait for the response"""
        self.socket.send((cmd + "\r\n").encode())

    def ping_handler(self):
        data = self.get_response()
        if data.find(b"PING") != -1:
            pong = data.decode().split(':')[1]
            self.socket.send(pong.encode())
            return "PING"
        else:
            return data.decode()

    def is_disconnected(self, data=bytes):
        clearedData = data.decode().split("\n")
        clearedData = clearedData[len(clearedData) - 2]
        if clearedData.startswith('ERROR :Closing link:') is True:
            self.connected = False
            return True
        else:
            return False
    
    def message_handling(self, msg):
        msg_array = msg.split("\r\n")
        for line in msg_array:
            print(line)
            if re.search(r" [4-5][0-9]{2} \* " + self.nickname, line):
                return False
        return True

    def __del__(self):
        if self.socket is not None:
            self.socket.close()