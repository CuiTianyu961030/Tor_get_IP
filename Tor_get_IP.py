from stem import Signal
from stem import StreamStatus
from stem.control import EventType, Controller
import functools
import socks
import socket
import requests
import time

def connectTor():
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150) #Linux 9050
    socket.socket = socks.socksocket

def renew_tor():
    controller.authenticate()
    controller.signal(Signal.NEWNYM)


def showmyip():
    r = requests.get('http://icanhazip.com/')
    ip_address = r.text.strip()
    print("src IP: %s\n" % (ip_address))

def stream_event(controller, event):
    if event.status == StreamStatus.SUCCEEDED and event.circ_id:
        print("dst IP: %s" % (event.target_address))

if __name__ == "__main__":
    controller = Controller.from_port(port=9151) #Linux 9051

    controller.authenticate()
    stream_listener = functools.partial(stream_event, controller)
    controller.add_event_listener(stream_listener, EventType.STREAM)

    for i in range(10):
        renew_tor()
        connectTor()
        showmyip()
        time.sleep(10)