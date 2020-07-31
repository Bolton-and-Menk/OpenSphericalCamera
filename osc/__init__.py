#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Haarm-Pieter Duiker'
__copyright__ = 'Copyright (C) 2016 - Duiker Research Corp'
__license__ = ''
__maintainer__ = 'Haarm-Pieter Duiker'
__email__ = 'support@duikerresearch.org'
__status__ = 'Production'

__major_version__ = '1'
__minor_version__ = '0'
__change_version__ = '0'
__version__ = '.'.join((__major_version__,
                        __minor_version__,
                        __change_version__))

from munch import munchify
##from osc import OpenSphericalCamera
##from theta import RicohThetaS
from .insta import Insta360Pro2

cams = munchify({
    'Insta360Pro2': Insta360Pro2,
    })

