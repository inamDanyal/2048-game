import socket  # used to create the server
import json  # used to receive commands from clients
import threading  # used to run 2 functions at the same time through threads


"""
Socket : Used to create the server
Json : Used to send and recieve commands to clients, it also faster then compressing text manually
Threading : Used to run multiple methods in parallel
"""

# When 1 Client - WAIT
# When 2 Client - RUN GAME

# Colours
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (100, 255, 100)


class Server:

    def __init__(self):

        self.hostName = socket.gethostname()
        self.HOST = socket.gethostbyname(self.hostName)
        self.PORT = 50000

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def binding(self):
        """
        Binds the host and port together
        :return:
        """

        print("[STARTING]")

        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)

        try:
            self.s.listen(1)
            print("Server is up and running waiting for the clients")

        except:
            print("ERROR - Binding has failed")

    @staticmethod
    def handle_connections(conn, client_id):
        """
        Recieves messages from the clients
        :param conn: the connection
        :param client_id: the client ID
        :return: nothing, prints out the moves made by each client in the format:
                                            "'client_id' {'COMMAND': 'MOVE', 'MOVE': {'DIRECTION': 'DIRECTION MOVED'}}
        """

        connected = True
        while connected:

            data = conn.recv(1024)  # receives the command

            if not data:
                pass

            else:

                msg = json.loads(data.decode())  # decodes the data

                # simplifying the message
                if msg == {'COMMAND': 'MOVE', 'MOVE': {'DIRECTION': 'LEFT'}}:
                    print("Client", str(client_id) + ",", "LEFT")

                elif msg == {'COMMAND': 'MOVE', 'MOVE': {'DIRECTION': 'RIGHT'}}:
                    print("Client", str(client_id) + ",", "RIGHT")

                elif msg == {'COMMAND': 'MOVE', 'MOVE': {'DIRECTION': 'UP'}}:
                    print("Client", str(client_id) + ",", "UP")

                elif msg == {'COMMAND': 'MOVE', 'MOVE': {'DIRECTION': 'DOWN'}}:
                    print("Client", str(client_id) + ",", "DOWN")

                else:
                    print(client_id, msg)

    def start_server(self):
        """
        Actual server
        :return:
        """

        self.binding()

        client_id = 1
        client_list = []

        while True:
            conn, addr = self.s.accept()  # Blocking statement sits here until the client connects
            print("Client Connected", addr)
            client_list.append(conn)  # adds the new connection to the list of clients

            threading.Thread(target=self.handle_connections, args=(conn, client_id)).start()  # threading

            client_id += 1

            if len(client_list) == 0:    # if the total amount of clients is 0 then wait
                print("[WAITING FOR ANOTHER PLAYER]")

                # WAITING_button.draw_button("WAITING FOR ANOTHER PLAYER", WHITE, GREEN, GRAY)

            if len(client_list) == 1:
                client_id = 1

                for client in client_list:
                    msg = {"COMMAND": "SETUP", "DATA": {"PlayerId": client_id}}
                    client.sendall(json.dumps(msg).encode())  # sends the message
                    client_id += 1



