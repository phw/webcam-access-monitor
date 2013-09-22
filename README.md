Webcam Access Monitor
=====================

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
For now there is no install script and you have to copy the individual
components into place manually. Have a look at the Arch Linux
[AUR package](https://aur.archlinux.org/packages/we/webcam-access-monitor/PKGBUILD)
for an example. I will add a proper install script and better instructions soon.
