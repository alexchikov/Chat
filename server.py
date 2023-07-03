import abc
import socket
import random
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


class Server(__BaseServer):
    def __init__(self, host: str = "localhost", port: int = random.randint(6000,9000), max_connections: int = 2) -> None:
        self.__host = host
        self.__port = port
        self.__max_connections = max_connections
        self.__users = []
        self.__usernames = []

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
            message = conn.recv(2048)
            self._send_message(message=message, sendler=conn)

    def _accept_connections(self):
        while True:
            conn, addr = self.__server.accept()
            print(f"{addr[0]} connected")
            self.__users.append(conn)
            # conn.recv(2048)
            
            receiver = Thread(target=self._recieve_message, args=(conn,))
            receiver.start()
        
    def start(self):
        acceptor = Thread(target=self._accept_connections)
        acceptor.start()


if __name__ == "__main__":
    s = Server()
    s.set_server()
    s.start()
