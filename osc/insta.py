# package info
__author__ = 'Phil Nagel'
__organization__ = 'Bolton & Menk, Inc.'
__author_email__ = 'philna@bolton-menk.com'
__website__ = None
__version__ = '0.1'
__package__ = None
__documentation__ = None
__keywords__ = []
__description__ = ''

import requests
from requests import Session
from munch import munchify

from .common import RepeatedTimer

class Insta360Pro2:
    """ Class to handle connections to the Insta 360 Pro 2 camera.

    Args:
        ip (str): Camera IP. Default is '192.168.1.188'

    """
    def __init__(self, ip='192.168.1.188'):
        self.ip = ip
        self.is_connected = False
        self.url = f'http://{self.ip}:20000/osc/commands/execute'
        self.stateurl = f'http://{self.ip}:20000/osc/state'
        self.fileurl = f'http://{self.ip}:8000/'
        self.S = Session()
        self.connect()
        self.keep_alive = RepeatedTimer(1, self.check_state)


    def do_post(self, url, *args, **kwargs):
        resp = self.S.post(url, *args, **kwargs)
        resp = munchify(resp.json)
        if resp.state == 'exception':
            raise RuntimeError(resp)
        else:
            return resp


    def connect(self):
        """ Initiate a connection to the camera.

        """
        resp = self.do_post(self.url, json={"name": "camera._connect"})
        if resp.Fingerprint:
            self.fingerprint = resp.result.Fingerprint
            self.S.headers.update({'Fingerprint': self.fingerprint})
            self.is_connected = True
            self.keep_alive.start()


    def disconnect(self):
        """ Disconnect from camera so other clients can connect.

        """
        self.keep_alive.stop()
        self.S = requests.Session()
        self.is_connected = False


    def check_state(self):
        """ Query the state endpoint. Must be done periodically to keep
        connection alive. Camera will disconnect if not polled for 10 secs.

        """
        resp = self.do_post(self.stateurl)
        return munchify(resp.json)



