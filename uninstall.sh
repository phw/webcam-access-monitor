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

echo -n "Uninstalling Gnome Shell extension..."
SHELL_EXTENSION_DIR=${PREFIX}/usr/share/gnome-shell/extensions/webcam-access-monitor@philipp.wolfer.co
rm -rf "${SHELL_EXTENSION_DIR}"
echo " done."

echo -n "Uninstalling DBUS service..."
rm "${PREFIX}"/usr/share/dbus-1/services/com.uploadedlobster.WebcamAccessMonitor.service
rm "${PREFIX}"/usr/lib/webcam-access-monitor/webcam-access-monitor.py
echo " done."

echo -n "Unnstalling Python modules..."
SITE_PACKAGES=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
PYTHON_MODULE_DIR=${PREFIX}${SITE_PACKAGES}/webcamaccessmonitor
rm -rf "${PYTHON_MODULE_DIR}"
echo " done."
