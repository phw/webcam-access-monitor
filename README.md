Webcam Access Monitor
=====================
[![GitHub release](https://img.shields.io/github/release/phw/webcam-access-monitor.svg)](https://github.com/phw/webcam-access-monitor/releases)
[![License: GPL v3+](https://img.shields.io/badge/license-GPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Code Climate](https://codeclimate.com/github/phw/webcam-access-monitor/badges/gpa.svg)](https://codeclimate.com/github/phw/webcam-access-monitor)

DEVELOPMENT STOPPED
-------------------
I am no longer actively developing this extension as I stopped using it myself. I originally set this up since my Laptop had a broken webcam LED, but since I moved to a new laptop this is not an issue anymore.

I don't think there are many users of this, but I will try to still fix bugs if they come up and accept pull requests. **If you are actually using this extension and want to take over maintenance, please let me know.**

About
-----
The Webcam Access Monitor helps you to see whether your webcam is currently
active or not. This is usefull if your webcam has no status LED and you want
to know if your webcam is currently watching you.

At the moment the Webcam Access Monitor consists of a D-Bus service which is
monitoring your computers camera and a Gnome Shell extension to display an
icon whenever a webcam is in use.

Using a D-Bus service makes it easy to extend this application to support
more desktop environments, such as the Unity desktop using an indicator applet
or good old notification applets.


Requirements
------------

* Python 3
* dbus-python
* pyinotify
* PyGObject
* PSmisc


Installation and usage
----------------------
A basic install script is included, that will install all the files to the
appropriate places in `/usr/`. Just run it as:

    ./install.sh

To uninstall again run:

    ./uninstall.sh

For Arch Linux you can also install using the
[AUR package](https://aur.archlinux.org/packages/webcam-access-monitor/).
