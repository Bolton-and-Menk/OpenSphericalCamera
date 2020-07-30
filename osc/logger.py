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
logger = logging.getLogger('osc')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)