from irc import Client
import select
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-ip", help="Adresse of the IRC server")
parser.add_argument("-port", type=int, help="Port of the IRC server (\"6667\" by default)", default=6667)
parser.add_argument("-n", "--nickname", help="Nickname (\"Guest\" by default)", default="Guest")
parser.add_argument("-f", "--fullname", help="Fullname (\"John Doe\" by default)", default="John Doe")
parser.add_argument("-p", "--password", help="Password (empty by default)", default="")
parser.add_argument("--noarg", help="Do not enter information via arguments but inside the program.", action="store_true")
args = parser.parse_args()

server = Client(args.ip, int(args.port), args.nickname, args.fullname, args.password)
if args.noarg is True:
    server.ask_config()
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
        if server.is_disconnected(data) is True:
            break
    if server.connected is False:
        continue
    for socket in writeable:
        if server.logged == False:
            server.login()
            time.sleep(1.1)
            message = socket.recv(8192).decode()
            if server.message_handling(message) is False:
                server.connected = False
            break
        while msg == "":
            msg = input("> ")
        server.send_command(msg)
        time.sleep(0.1)
        msg = ""