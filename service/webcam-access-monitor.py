#!/bin/env python

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

if __name__ == '__main__':
    import dbus
    from gi.repository import GObject
    from dbus.mainloop.glib import DBusGMainLoop
    from webcamaccessmonitor.dbus import WebcamStatusService, BUS_NAME, OBJECT_PATH
    from webcamaccessmonitor.webcammonitor import WebcamMonitor
    
    loop = GObject.MainLoop()
    GObject.threads_init()
    DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    name = dbus.service.BusName(BUS_NAME, bus)
    dbus_service = WebcamStatusService(bus, OBJECT_PATH)
    with WebcamMonitor("/dev/video*", dbus_service) as webcam_monitor:
        loop.run()
 
