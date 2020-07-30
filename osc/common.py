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


import logging
from threading import Timer

import netifaces
from munch import munchify

#from .theta import RicohThetaS
from .logger import logger

CAMERAS = munchify({
    'Insta360Pro2': {
        'IPs': ['192.168.1.188'],
        'name': 'Insta360 Pro 2',
        'classname': 'Insta360Pro2'
        },
    'Theta': {
        'IPs': ['192.168.1.1'],
        'name': 'Ricoh Theta',
        'classname': 'RicohThetaS'
        },
    'Test': {
        'IPs': ['192.168.15.1'],
        'name': 'test',
        'classname': 'Test'
        }
})




def iter_gateway_ips():
    """
    Returns:
        Yields all gateway IP addresses in the IPv4 and IPv6 spaces.

    """
    inets = [netifaces.AF_INET, netifaces.AF_INET6]
    for inet in inets:
        gwy_tuples = netifaces.gateways().get(inet)
        if gwy_tuples:
            for tup in gwy_tuples:
                yield tup[0]


class Test:
    def __init__(self):
        self.test = 'test'

def find_cameras():
    """ Try to detect spherical cameras attached to network interfaces.

    Returns:
        List of munches:
            {'IP': IP to reach the camera,
             'name':  Name of camera,
             'camera': Uninitialized camera class
             }

    """
    cams = []
    gateways = list(iter_gateway_ips())
    logger.debug(f'Gateways found: {gateways}')
    for cam in CAMERAS.values():
        logger.debug(f'  Checking IPs for {cam.name}')
        for ip in cam.IPs:
            logger.debug(f'    Trying IP {ip}')
            if ip in gateways:
                logger.info(f'  **IP {ip} matches {cam.name}')
                cam_munch = munchify({
                    'IP': ip,
                    'name': cam.name,
                    'camera': globals()[cam.classname]
                })
                cams.append(cam_munch)
    return cams


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.is_waiting = False


    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)


    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


if __name__ == '__main__':
    pass