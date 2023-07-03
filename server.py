import abc
import socket
import random
import pickle
from threading import Thread


class __BaseServer(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def set_server(self):
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

    def set_server(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__host, self.__port,))
        print(f"Server's working on {self.__host} ip and {self.__port} port")
        self.__server.listen(self.__max_connections)

    def _send_message(self, message: str, sendler):
        for conn in self.__users:
            if conn != sendler:
                conn.send(message)
                
    def _recieve_message(self, conn):
        while True:
            try:
                message = conn.recv(2048)
                data = pickle.dumps((self.__usernames[conn], message,))
                self._send_message(message=data, sendler=conn)
            except:
                conn.close()
                del self.__usernames[conn]
                self.__users.remove(conn)

    def _accept_connections(self):
        while True:
            conn, addr = self.__server.accept()
            print(f"{addr[0]} connected")
            self.__users.append(conn)
            
            username = conn.recv(2048)
            self.__usernames.setdefault(conn, username)

            receiver = Thread(target=self._recieve_message, args=(conn,))
            receiver.start()

    def start(self):
        acceptor = Thread(target=self._accept_connections)
        acceptor.start()


if __name__ == "__main__":
    s = Server(max_connections=5)
    s.set_server()
    s.start()