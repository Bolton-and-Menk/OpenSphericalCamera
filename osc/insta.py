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
import datetime
import json
import os
from requests import Session
from munch import munchify

from osc.common import RepeatedTimer
from osc.logger import logger


class Insta360Pro2:
    """ Class to handle connections to the Insta 360 Pro 2 camera.
    Full REST API docs: https://github.com/Insta360Develop/ProCameraApi

    Args:
        ip (str): Camera IP. Default is '192.168.1.188'

    """
    def __init__(self, ip='192.168.1.188'):
        self.ip = ip
        self.url = f'http://{self.ip}:20000/osc/commands/execute'
        self.stateurl = f'http://{self.ip}:20000/osc/state'
        self.infourl = f'http://{self.ip}:20000/osc/info'
        self.fileurl = f'http://{self.ip}:8000/'
        self.S = Session()
        self.keep_alive = RepeatedTimer(1, self.check_state)
        self._attrs = ['gps', 'gps_signal', 'is_connected', 'battery_level',
                     'battery_charging', 'capturing', 'info', 'is_capturing']
        for attr in self._attrs:
            setattr(self, attr, False)


    def do_post(self, url, *args, **kwargs):
        resp = self.S.post(url, *args, **kwargs)
        if resp.ok:
            resp = munchify(resp.json())
            logger.debug(resp)
            if resp.state == 'exception':
                raise RuntimeError(resp)
            else:
                return resp
        else:
            raise RuntimeError(resp)


    def async_post(self, url, *args, **kwargs):
        pass


    def connect(self):
        """ Initiate a connection to the camera.

        """
        timetemplate = '%m%d%H%M%Y.%S'
        tzoffset = datetime.datetime.now() - datetime.datetime.utcnow()
        m, _ = divmod(tzoffset.total_seconds(), 60)
        h, m = [int(i) for i in divmod(m, 60)]
        tzstr = "GMT{h_value:+0{h_width}d}:{m_value:0{m_width}d}".format(
                h_value=h, h_width=3, m_value=m, m_width=2)
        params = {
            "name":"camera._connect",
            "parameters":{
                "time_zone": tzstr,
                "date_time": datetime.datetime.utcnow().strftime(timetemplate),
                "hw_time": datetime.datetime.utcnow().strftime(timetemplate)
                }}
        resp = self.do_post(self.url, json=params)
        if resp.results.Fingerprint:
            self.fingerprint = resp.results.Fingerprint
            self.S.headers.update({'Fingerprint': self.fingerprint})
            self.is_connected = True
            self.keep_alive.start()
            self.get_info()
        return


    def disconnect(self):
        """ Disconnect from camera so other clients can connect.

        """
        self.keep_alive.stop()
        resp = self.do_post(self.url, json={"name": "camera._disconnect"})
        self.S = requests.Session()
        self.is_connected = False
        return


    def check_state(self):
        """ Query the state endpoint. Must be done periodically to keep
        connection alive. Camera will disconnect if not polled for 10 secs.

        """
        resp = self.do_post(self.stateurl)
        self.battery_level = resp.state._battery.battery_level
        self.battery_level = resp.state._battery.battery_charge
        self.gps = True if resp.state._gps_state > 1 else False
        self.gps_signal = resp.state._gps_state
        if resp.state._cam_state != 0:
            self.is_capturing = True
        else:
            self.is_capturing = False
        return


    def get_info(self):
        self.info = self.do_post(self.infourl)
        return self.info


    def take_picture(self):
        params = {
          "name": "camera._takePicture",
          "parameters":{
            "origin":{
              "mime":"jpeg",
              "width":4000,
              "height":3000,
              "saveOrigin":True,
            }
            }}
        resp = self.do_post(self.url, json=params)


    def start_interval(self, interval):
        """ Start an interval capture.

        Args:
            interval (int): Time interval in ms.

        """
        params = {
            'name': 'camera._startRecording',
            'parameters': {'fileOverride': False,
            'origin': {'hdr': False,
                       'height': 3000,
                       'logMode': 0,
                       'mime': 'jpeg',
                       'saveOrigin': True,
                       'width': 4000},
            'stabilization': False,
            'storageSpeedTest': False,
            'timelapse': {'enable': True, 'interval': 2000}}}
        resp = self.do_post(self.url, json=params)
        return resp


    def stop_interval(self):
        if self.is_capturing:
            resp = self.do_post(self.url, json={'name': 'camera._startRecording'})
            return resp


    def __repr__(self):
        if self.is_connected:
            strdct = {attr: getattr(self, attr) for attr in self._attrs}
            strdct['ip'] = self.ip
        else:
            strdct = {'is_connected': self.is_connected,
                'ip': self.ip}
        return 'Insta 360 Pro 2 Handler Class' + os.linesep + json.dumps(strdct, indent=2)
