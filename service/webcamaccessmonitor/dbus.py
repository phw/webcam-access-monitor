# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Philipp Wolfer <ph.wolfer@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus, dbus.service
from webcamaccessmonitor import STATE_UNKNOWN

BUS_NAME = "com.uploadedlobster.WebcamAccessMonitor"
INTERFACE_NAME = "com.uploadedlobster.WebcamAccessMonitor"
OBJECT_PATH = "/com/uploadedlobster/WebcamAccessMonitor"

class WebcamStatusService(dbus.service.Object):
    def __init__(self, bus, object_path):
        self.device_states = {}
        dbus.service.Object.__init__(self, bus, object_path)


    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='i')
    def getDeviceState(self, device):
        return self.device_states.get(device, STATE_UNKNOWN)


    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='a{si}')
    def getAllDeviceStates(self):
        return self.device_states


    @dbus.service.signal(dbus_interface=INTERFACE_NAME,
                         signature='(si)')
    def stateChanged(self, state_tuple):
        (device, state) = state_tuple
        print("DEBUG: Webcam %s status set %d" % (device, state))
        self.device_states[device] = state
