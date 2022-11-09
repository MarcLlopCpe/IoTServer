# Program to control gateway between Android application
# and microcontroller through USB tty
import datetime

import constantes as cst
import tools.serial as tl_ser
import tools.udp as tl_udp


def print_sep(sep: str = "==================", end="\n"):
    print(sep, end=end)


class LastValue:
    val = []
    order = "TL"

    def __str__(self) -> str:
        return ",".join([self.order[i] + ":" + str(self.val[i]) for i in range(len(self.val))])

    def set(self, val: [], order="TL"):
        self.val = val
        self.order = order

    def get(self):
        return self.val


class MessageTreatmentException(Exception):
    pass


class Main:

    def __init__(self) -> None:
        self.last_value = LastValue()

        self.f = open(cst.FILENAME, "a")

        self.serial = tl_ser.init()

        self.server, self.server_thread = tl_udp.init(self.serial, self.last_value)

        super().__init__()

    def __message_treatment(self, message):

        # message = self.serial.read(cst.SENSOR_DATA_LENGTH)

        header: str = message[1:3].decode()
        data: bytes = message[3:-2]

        print(header, datetime.datetime.now().strftime("%H:%M:%S"), ':')

        ret = []

        for key in header:
            print(">", key, end=" = ")
            size, converter = tl_ser.conversion_mapper[key]

            if len(data) > size:
                data_to_decode, data = tl_ser.cut_chain(data, size)
            elif len(data) == size:
                data_to_decode = data
                data = b""
            else:
                raise MessageTreatmentException("Data length is inferior => parsing is interrupt")

            decoded_data = converter(data_to_decode)
            print(decoded_data)
            ret.append(decoded_data)

        if len(data) != 0:
            # print(data, ret)
            raise MessageTreatmentException("Data length is superior => parsing is interrupt")

        return header, ret

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.f.close()
        self.serial.close()
        exit()

    def start(self):

        try:
            self.server_thread.start()

            print(f"Server started at {cst.HOST} port {cst.UDP_PORT}")
            print_sep()

            while self.serial.isOpen():
                if self.serial.inWaiting() >= cst.SENSOR_DATA_LENGTH:  # if incoming bytes are waiting
                    message = self.serial.read_until(b'\n')

                    if len(message) == cst.SENSOR_DATA_LENGTH:
                        try:
                            order, new_value = self.__message_treatment(message)
                            self.last_value.set(new_value, order=order)
                        except MessageTreatmentException as e:
                            print(e.with_traceback)
                    else:
                        print("message incomplet -> ignoré")

                    print_sep()

                # value_split = data_str_decode.split(";")
                # print(value_split)
        except (KeyboardInterrupt, SystemExit):
            self.close()


# Main program logic follows:
if __name__ == '__main__':
    print("__Début__")
    Main().start()
    print("__Fin__")
