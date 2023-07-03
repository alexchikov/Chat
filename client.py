import abc
import socket
from threading import Thread


class __BaseClient(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    async def _send_message(self, message: str):
        pass

    @abc.abstractmethod
    async def _receive_message(self):
        pass

    @abc.abstractmethod
    async def start(self):
        pass


class Client(__BaseClient):
    def __init__(self, username: str, host: str, port: int) -> None:
        self.username = username
        self.__host = host
        self.__port = port
        self.__other_users = []
        
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__host, self.__port,))

    def _send_message(self):
        while True:
            message = input(f"({self.username}): ")
            encoded_message = message.encode()
            self.__client.send(encoded_message)

    def _receive_message(self):
        while True:
            message = self.__client.recv(2048)
            print("(not me): " + message.decode())

    def start(self):
        receiver = Thread(target=self._receive_message)
        receiver.start()
        sendler = Thread(target=self._send_message)
        sendler.start()
    

if __name__ == "__main__":
    c = Client(input("Your username: "), input("Host: "), int(input("Port: ")))
    c.start()
