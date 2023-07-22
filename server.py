import abc
import socket
import random
import pickle
import logging
import sys
from threading import Thread


class __BaseServer(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def _send_message(self, message: str):
        pass

    @abc.abstractmethod
    def _recieve_message(self):
        pass
    
    @abc.abstractmethod
    def _accept_connections(self):
        pass
    
    @abc.abstractmethod
    def start(self):
        pass


class Server(__BaseServer):
    def __init__(self, host: str = "localhost", port: int = random.randint(6000, 9000), max_connections: int = 2) -> None:
        self.__host = host
        self.__port = port
        self.__max_connections = max_connections
        self.__users = []
        self.__usernames = dict()
        
        self.__receivers = dict()
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(levelname)s %(asctime)s: %(message)s")

    def set_server(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((self.__host, self.__port,))
        logging.info(f"Server's working on {self.__host} ip and {self.__port} port")
        self.__server.listen(self.__max_connections)

    def _send_message(self, message: str, sendler):
        for conn in self.__users:
            if conn != sendler:
                try:
                    conn.send(message)
                    logging.info(f"send message to {self.__usernames[conn].decode()} from {self.__usernames[sendler].decode()}")
                except (ConnectionError, OSError):
                    self.__usernames.pop(sendler)
                    self.__users.remove(sendler)
                    sendler.close()
                    break
                
    def _recieve_message(self, conn):
        flag = True
        while flag:
            try:
                message = conn.recv(2048)
                data = pickle.dumps((self.__usernames[conn], message,))
                self._send_message(message=data, sendler=conn)
            except (OSError, ConnectionResetError):
                self.__usernames.pop(conn)
                self.__users.remove(conn)
                conn.close()
                flag = False
                break
                
    def _accept_connections(self):
        while True:
            conn, addr = self.__server.accept()
            logging.info(f"user {addr[0]} connected")
            self.__users.append(conn)
            
            username = conn.recv(2048)
            self.__usernames.setdefault(conn, username)

            receiver = Thread(target=self._recieve_message, args=(conn,))
            self.__receivers[conn] = receiver
            self.__receivers[conn].start()

    def start(self):
        acceptor = Thread(target=self._accept_connections)
        acceptor.run()


if __name__ == "__main__":
    s = Server(max_connections=5)
    s.set_server()
    s.start()