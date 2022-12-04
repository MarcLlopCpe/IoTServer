import socketserver
import threading
from typing import Any

import constantes as cst
import tools.serial as tl_ser
from main import LastValue


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    currentThread: threading.Thread

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.current_thread = None

    def print(self, *messages: str, sep=", ", end="\n"):
        print(self.current_thread.name + ", ", sep.join(messages), end="\n")

    def send_serial(self, data):
        message = b"-" + data + b"\r\n"
        tl_ser.send_uart_message(self.server.serial[0], message)
        self.print(f"Serial wrote: {message}", end="")

    def send_udp_last_value(self, socket):
        data: LastValue = self.server.serial[1]
        # TODO REGLER PROBLEME DE PORT
        print(str(data).encode(), *self.client_address)
        socket.sendto(str(data).encode(), self.client_address)
        self.print("UDP send: " + str(data))

    def handle(self):
        self.current_thread = threading.current_thread()

        data: bytes = self.request[0].strip()
        socket = self.request[1]

        self.print(f"client: {self.client_address}", f"received: {data}")

        if len(data) != 0:
            if data in cst.MICRO_COMMANDS:  # Send message through UART
                self.send_serial(data)
            elif data.startswith(b"getValues("):  # Sent last value received from micro-controller
                self.send_udp_last_value(socket)
            else:
                self.print("Unknown message: " + str(data))
        print()


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):

    def __init__(self, server_address: Any, serial: tuple, RequestHandlerClass):
        self.serial = serial
        super().__init__(server_address, RequestHandlerClass)


def init(serial, last_value: LastValue):
    server = ThreadedUDPServer((cst.HOST, cst.UDP_PORT), (serial, last_value), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    return server, server_thread
