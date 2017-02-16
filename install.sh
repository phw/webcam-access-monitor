#!/usr/bin/env sh

if [ -z  "$1" ]; then
    PREFIX=/usr
else
    PREFIX=$1
fi

if [ "$PREFIX" = "/usr" ] && [ "$(id -u)" != "0" ]; then
  # Make sure only root can run our script
  echo "This script must be run as root to install to ${PREFIX}" 1>&2
  exit 1
fi

BASEDIR=$(dirname "$0")
SITE_PACKAGES=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

echo -n "Installing Gnome Shell extension..."
SHELL_EXTENSION_DIR=${PREFIX}/usr/share/gnome-shell/extensions/webcam-access-monitor@philipp.wolfer.co
install -d "${SHELL_EXTENSION_DIR}"
install "${BASEDIR}"/gnome-shell-extension/*.{js,json,css} "${SHELL_EXTENSION_DIR}"
echo " done."

echo -n "Installing Python modules..."
PYTHON_MODULE_DIR=${PREFIX}${SITE_PACKAGES}/webcamaccessmonitor
install -d "${PYTHON_MODULE_DIR}"
install "${BASEDIR}"/service/webcamaccessmonitor/*.py "${PYTHON_MODULE_DIR}"
echo " done."

echo -n "Installing DBUS service..."
install -D "${BASEDIR}"/service/com.uploadedlobster.WebcamAccessMonitor.service "${PREFIX}"/usr/share/dbus-1/services/com.uploadedlobster.WebcamAccessMonitor.service
install -D "${BASEDIR}"/service/webcam-access-monitor.py "${PREFIX}"/usr/lib/webcam-access-monitor/webcam-access-monitor.py
echo " done."
