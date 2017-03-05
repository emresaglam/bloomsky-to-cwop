import socket
import requests
from datetime import datetime, date, time
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Take Bloomsky device data and push it to CWOP.')
parser.add_argument('--config', '-c', default='config.json')
args=parser.parse_args()

class Connect(object):

    def __init__(self, IP, port):
        self.IP = IP
        self.port = port

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        #print('connecting to host')
        try:
            sock.connect((self.IP, self.port))
        except:
            print "Unable to connect!"
            sys.exit()
        #print "Connected to %s on port %s" % (self.IP, self.port)
        return sock

    def send(self, command):
        sock = self.connect()

        #print('sending: ' + command)
        sock.sendall(command)

    def close(self):
        #print "Disconnecting from %s" % self.IP
        sock.shutdown()
        sock.close()


with open(args.config, "r") as f:
    conf = json.loads(f.read())

STATION_TYPE = conf["station"]["type"]
STATION_NAME = conf["station"]["name"]
STATION_PASS = conf["station"]["pass"]
STATION_LATITUDE = conf["station"]["latitude"]
STATION_LONGITUDE = conf["station"]["longitude"]
APRS_SERVER = conf["aprs"]["server"]
APRS_PORT = conf["aprs"]["port"]
BUFFER_SIZE = 1024

now = datetime.now()
nowh = now.strftime("%H%M%S")


def make_aprs_wx(wind_dir=None, wind_speed=None, wind_gust=None, temperature=None, rain_since_midnight=None,
                 humidity=None, pressure=None):
    """
    Assembles the payload of the APRS weather packet.
    """

    def str_or_dots(number, length):
        """
        If parameter is None, fill space with dots. Else, zero-pad.
        """
        if number is None:
            return '0' * length
        else:
            format_type = {
                'int': 'd',
                'float': '.0f',
            }[type(number).__name__]
            return ''.join(('%0', str(length), format_type)) % number

    return '%s>APRS,TCPIP*,qAC,CWOP-2:@%sz%s/%s_%s/%sg%st%sP%sh%sb%s%s' % (
        STATION_NAME,
        nowh,
        STATION_LATITUDE,
        STATION_LONGITUDE,
        str_or_dots(wind_dir, 3),
        str_or_dots(wind_speed, 3),
        str_or_dots(wind_gust, 3),
        str_or_dots(temperature, 3),
        str_or_dots(rain_since_midnight, 3),
        str_or_dots(humidity, 2),
        str_or_dots(pressure, 5),
        STATION_TYPE
    )

def get_bloomsky_data():
    header = {"Authorization": conf["bloomsky"]["api_key"]}
    r = requests.get(conf["bloomsky"]["url"], headers = header)
    bloomskyData = r.json()
    return bloomskyData

bloomskyData = get_bloomsky_data()


login = "user %s pass %s vers Test\n" % (STATION_NAME, STATION_PASS)
aprs_packet = make_aprs_wx(temperature=bloomskyData[0]["Data"]["Temperature"], humidity=bloomskyData[0]["Data"]["Humidity"], pressure=bloomskyData[0]["Data"]["Pressure"])


connect = Connect(IP=APRS_SERVER, port=APRS_PORT)
#print connect.send(login + aprs_packet + "\n")
connect.send(login + aprs_packet + "\n")

sys.exit()
