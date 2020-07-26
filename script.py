from irc import Client

server = Client("irc.root-me.org", 6667, "Freestyle", "FreestyleG")
server.connect()

logged_in = False
i = 0

while server.connected is True:
    if server.logged is False:
        server.login()
        server.join("#root-me_challenge")
    msg = input("> ")
    ret = server.sendCommand(msg)