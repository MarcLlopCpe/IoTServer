from pathlib import Path

# === DETECTION DU RELAY === #
_user = "marc.llop"

_MICROBIT_MNT_PATH: Path = Path(f"/run/media/{_user}/")
_MICROBIT_DETAILS_FILE: Path = Path("DETAILS.TXT")

MICROBIT_PATHS: (Path, Path) = (
    _MICROBIT_MNT_PATH / Path("MICROBIT") / _MICROBIT_DETAILS_FILE,
    _MICROBIT_MNT_PATH / Path("MICROBIT1") / _MICROBIT_DETAILS_FILE
)

MICROBIT_RELAY_ID: str = "9901000051774e45007670100000004a0000000097969901"

# === TRANSMISSION SÉRIE === #

SERIALPORT = "/dev/ttyACM1"
BAUDRATE = 115200

ORDER_DATA_LENGTH = 1 + 2 * 1
SENSOR_DATA_LENGTH = ORDER_DATA_LENGTH + 2 * 4 + 2

# === SERVER UDP === #

HOST = ""
UDP_PORT = 10000
MICRO_COMMANDS = [B"TL", B"LT"]
FILENAME = "values.txt"

# === INFLUXDB === #

ORG = "CPE"
URL = "http://localhost:8086"
BUCKET="IOT"

Mesures = {
    'T':"temperature",
    'L':"lumiere"
}