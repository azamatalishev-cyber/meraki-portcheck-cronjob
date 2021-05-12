#!/usr/bin/env python3.7

from decouple import AutoConfig
# from http.client import HTTPConnection
from pprint import pprint
from time import strftime
import logging
import meraki
import os
import requests
import sys


cwd = os.path.dirname(os.path.abspath("__file__"))

dir_path = os.path.dirname(os.path.realpath(__file__))

if cwd != dir_path:
    os.chdir(dir_path)
    print(os.getcwd())

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = logging.FileHandler(filename='./logs/meraki-portcycle.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

date_strftime_format = "%Y-%m-%d %H:%M:%S"
message_format = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=message_format,
    datefmt=date_strftime_format,
    handlers=handlers
)

logger = logging.getLogger('LOGGER_NAME')

config = AutoConfig(os.getcwd())
env = os.getcwd() + '/.env'

if os.path.exists(env):
    API_KEY = config('API_KEY')
    SNITCH_URL = config('SNITCH_URL')
else:
    API_KEY = os.getenv('API_KEY')
    SNITCH_URL = os.getenv('SNITCH_URL')

serial = 'Q2VX-K5M5-7ZV6'
ports = ['28']
dashboard = meraki.DashboardAPI(API_KEY, output_log=False)


# TODO: add counter to `get_port_status` to get an average of Kbps instead of one reading
def get_port_status(switch_serial, port):
    return dashboard.switch.getDeviceSwitchPortsStatuses(switch_serial)[port][
        'trafficInKbps']['total']


def cycle_ports(switch_serial, list_of_ports):
    return dashboard.switch.cycleDeviceSwitchPorts(switch_serial,
                                                   list_of_ports)


def dead_man_snitch():
    # HTTPConnection.debuglevel = 1
    x = requests.post(SNITCH_URL)
    if x.status_code >= 202:
        logger.info(f"POST Dead Man's Snitch - {x.status_code} ACCEPTED")
    elif x.status_code >= 200:
        logger.info(f"POST Dead Man's Snitch - {x.status_code} OK")
    else:
        logger.error(f"Was unable to POST to Dead Man's Snitch with status code {x.status_code} ")
        sys.exit(1)


def main():
    port_status = get_port_status(switch_serial=serial, port=28 - 1)
    try:
        if port_status <= 40.0:
            logger.info(f"Port 28 is clocked at {port_status} Kbps. Power cycling now ")
            cycle_ports(switch_serial=serial, list_of_ports=ports)
        elif port_status > 40.0:
            logger.info(f"Port 28 is clocked at {port_status} Kbps. Steady as she goes ")
    except Exception as e:
        logger.exception("Uncaught error. Exiting ")
        sys.exit(1)
    finally:
        dead_man_snitch()
        logger.info("Exiting successfully ")
        sys.exit(0)


if __name__ == "__main__":
    main()
