import socket
import json
import threading

"""
Socket : Used to connect to the server
Json : Used to send and recieve commands to clients, it also faster then compressing text manually
Threading : Used to run multiple methods in parallel
"""


# Client class
class Client:

    def __init__(self):

        self.HOST = '127.0.0.1'
        self.PORT = 50000

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.playerID = 0

    def start_conn(self):
        """
        Used to connect to the server
        :return:
        """
        
        self.s.connect((self.HOST, self.PORT))

    def receive(self):
        """
        Used to receive messages
        :return: nothing
        """

        print("[LISTENING]")

        while True:

            data = self.s.recv(1024)

            if not data:
                continue

            else:
                msg = json.loads(data.decode())
                print(msg)

    def main_conn(self):
        """
        Used to interpret commands and assign the player ID
        :return: nothing
        """

        self.start_conn()

        msg = json.loads(self.s.recv(1024).decode())  # bytes -> string -> dict

        # print(msg)
        while msg["COMMAND"] == "WAIT":
            print("[WAITING FOR OTHER PLAYER]")
            data = self.s.recv(1024)
            if not data:
                continue
            else:
                msg = json.loads(data.decode())

        self.playerID = msg["DATA"]["PlayerId"]
        print("your playerID is:", self.playerID)

        threading.Thread(target=self.receive).start()

    def send(self, msg):
        """
        Sends the message to the server
        :param msg: the message that will be sent
        :return: nothing
        """

        self.s.sendall(json.dumps(msg).encode())
