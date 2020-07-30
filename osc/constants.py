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

from munch import munchify

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