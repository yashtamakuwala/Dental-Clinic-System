# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.timeslots import Timeslots
from .api.bookings import Bookings
from .api.bookings_id import BookingsId


routes = [
    dict(resource=Timeslots, urls=['/timeslots'], endpoint='timeslots'),
    dict(resource=Bookings, urls=['/bookings'], endpoint='bookings'),
    dict(resource=BookingsId, urls=['/bookings/<id>'], endpoint='bookings_id'),
]