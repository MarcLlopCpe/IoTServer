import typing

import serial

import constantes as cst


def init():
    """
    init UART and return serial object
    :return:
    """
    ser = serial.Serial()

    # ser = serial.Serial(SERIALPORT, BAUDRATE)
    ser.port = cst.SERIALPORT
    ser.baudrate = cst.BAUDRATE
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = None  # block read

    # ser.timeout = 0             #non-block read
    # ser.timeout = 2              #timeout block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    # ser.writeTimeout = 0     #timeout for write
    print('Starting Up Serial Monitor')
    try:
        ser.open()
    except serial.SerialException:
        print("Serial {} port not available".format(cst.SERIALPORT))
        exit()

    return ser


def send_uart_message(ser, msg):
    ser.write(msg)
    print(f"Message <{msg}> sent to micro-controller.")


def get_messages():
    return


T = typing.TypeVar("T", str, bytes)


def cut_chain(b: T, pos: int) -> [T, T]:
    return [b[:pos], b[pos:]]


def to_unsigned_int(b: bytes):
    return int.from_bytes(b, "little", signed=False)


def to_int(b: bytes):
    return int.from_bytes(b, "little", signed=True)


def temperature_convertor(b: bytes):
    return to_int(b) / 100


conversion_mapper: dict[str, tuple[int, typing.Callable]] = {
    "T": (4, temperature_convertor),
    "L": (4, to_unsigned_int),
}
