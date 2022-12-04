import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import constantes as cst

def connexion_client(url=cst.URL, org=cst.ORG):
    # Connexion sur le serveur
    client = influxdb_client.InfluxDBClient(url, org)
    return client

def send_measurement(client, **kwargs):

    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point.from_dict(kwargs, WritePrecision.S)

    # Envoie des données
    write_api.write(bucket=cst.BUCKET, org=cst.ORG, record=point)