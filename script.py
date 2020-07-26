from irc import Client
import select
import time

server = Client("irc.root-me.org", 6667, "Freestyle", "FreestyleG")
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