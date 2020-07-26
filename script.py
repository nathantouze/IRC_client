from irc import Client
import select
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ip", help="Adresse of the IRC server")
parser.add_argument("port", type=int, help="Port of the IRC server")
parser.add_argument("-n", help="Nickname (\"Guest\" by default)", default="Guest")
parser.add_argument("--fullname", help="Fullname (\"John Doe\" by default)", default="John Doe")
parser.add_argument("-p", help="Password (empty by default)", default="")
args = parser.parse_args()

server = Client(args.ip, int(args.port), args.n, args.fullname, args.p)
server.connect()

msg = ""

while server.connected is True:
    try:
        readable, writeable, xset = select.select([server.socket], [server.socket], [], 0.1)
    except select.error:
        pass
    for socket in readable:
        data = socket.recv(8192)
        print(data.decode())
        if server.isDisconnected(data) is True:
            break
    if server.connected is False:
        continue
    for socket in writeable:
        if server.logged == False:
            server.login()
            time.sleep(1.1)
            print(socket.recv(8192).decode() + "\nYou are logged in !\n\n")
            break
        while msg == "":
            msg = input("> ")
        server.sendCommand(msg)
        time.sleep(0.1)
        msg = ""