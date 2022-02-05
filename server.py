import pickle
import socket
import threading


class ThreadedClient(threading.Thread):
    """
    ThreadedClient class handles the client requests and return appropriate responses.
    """
    def __init__(self, conn, p, gameID):
        threading.Thread.__init__(self)
        self.conn = conn
        self.player = p
        self.gameID = gameID

    def run(self):
        """
        Thread instructions to call.
        """
        while True:
            try:
                data = self.conn.recv(4096).decode()
            except:
                break
            if gameID in games:
                if not data:
                    break
                else:
                    if data == "go":
                        games[self.gameID]["state"] = "gameover"
                        self.conn.send(pickle.dumps(games[self.gameID]["playersPoints"]))
                    elif data == "get-points":
                        self.conn.send(pickle.dumps(games[self.gameID]["playersPoints"]))
                    elif data[0:11] == "set-points:":
                        games[self.gameID]["playersPoints"][self.player] = int(data[11:])
                        print("Player", self.player, "from game", self.gameID, "set his points to", data[11:])
                        self.conn.send("1".encode())
                    elif data == "get-state":
                        self.conn.send(games[self.gameID]["state"].encode())
                    elif data == "get-player":
                        self.conn.send(pickle.dumps(self.player))
                    elif data == "quit":
                        games[self.gameID]["state"] = "quit"
                        break
                    else:
                        break
            else:
                break
        print("Lost connection")
        try:
            del games[self.gameID]
            print("Terminating game", self.gameID)
        except:
            print("Error deleting game", self.gameID, "or game already deleted")
        global idCount
        idCount -= 1
        self.conn.close()


server = "127.0.0.1"
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind((server, port))
except socket.error as err:
    print(err)

sock.listen()
print("Server started, now waiting connection..")

global idCount
games = {}
idCount = 0

while True:
    conn, addr = sock.accept()
    print(addr[0], "connected")

    idCount += 1
    p = 0
    gameID = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameID] = {
            "playersPoints": [0, 0],
            "state": "waiting",
        }
        newThread = ThreadedClient(conn, 0, gameID)
    else:
        games[gameID]["state"] = "running"
        newThread = ThreadedClient(conn, 1, gameID)
    newThread.start()
