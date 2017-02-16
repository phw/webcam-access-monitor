# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, 2017 Philipp Wolfer <ph.wolfer@gmail.com>
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

import os
import glob
import subprocess
import pyinotify
from webcamaccessmonitor import STATE_UNKNOWN, STATE_OFF, STATE_ON


def _check_initial_camera_state(device):
    print("DEBUG: Checking device %s" % device)
    if not os.path.exists(device) \
       or not os.access(device, os.R_OK):
        return STATE_UNKNOWN

    process = subprocess.Popen(["fuser", device],
                               stdout=subprocess.PIPE)
    result = process.stdout.read()
    process.terminate()

    if result:
        return STATE_ON
    else:
        return STATE_OFF


class WebcamMonitor:

    def __init__(self, device_path, dbus_service):
        self.dbus_service = dbus_service

        self.mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE | \
            pyinotify.IN_DELETE_SELF | pyinotify.IN_OPEN | \
            pyinotify.IN_ATTRIB

        self.watch_descriptors = {}
        self.watch_manager = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.watch_manager)
        self.notifier.start()

        devices = glob.glob(device_path)

        for device in devices:
            watch_descriptor = self.watch_manager.watch_transient_file(
                device, self.mask, self._event_handler)
            self.watch_descriptors[device] = watch_descriptor

            state = _check_initial_camera_state(device)
            self.dbus_service.stateChanged((device, state))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for wd in self.watch_descriptors.values():
            for i in wd.values():
                self.watch_manager.rm_watch(i)
        self.notifier.stop()

    def _event_handler(self, pevent):
        # watch_manager.watch_transient_file expects a class
        # of type pyinotify.ProcessEvent, which it will instantiate
        # with the default constructor. This wrapper method
        # adds a reference to dbus_service the instance.
        return WebcamProcessEvent(pevent, dbus_service=self.dbus_service)


class WebcamProcessEvent(pyinotify.ProcessEvent):

    def my_init(self, **kargs):
        self.dbus_service = kargs['dbus_service']

    def process_default(self, event):
        device = event.pathname
        print("DEBUG: Event %s on device %s" % (event.maskname, device))
        state = None
        if event.mask & pyinotify.IN_OPEN:
            state = STATE_ON
        elif event.mask & pyinotify.IN_CLOSE_WRITE \
                or event.mask & pyinotify.IN_CLOSE_NOWRITE \
                or event.mask & pyinotify.IN_DELETE_SELF:
            state = STATE_OFF
        elif event.mask & pyinotify.IN_ATTRIB:
            # The permissions might have changed,
            # check the current state again
            state = _check_initial_camera_state(device)

        if state is not None:
            self.dbus_service.stateChanged((device, state))
