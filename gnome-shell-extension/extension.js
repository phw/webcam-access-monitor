/*
Copyright (c) 2013-2017 Philipp Wolfer <ph.wolfer@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/* exported init */

'use strict'

const Main = imports.ui.main
const PanelMenu = imports.ui.panelMenu
const Gio = imports.gi.Gio
const Lang = imports.lang
const St = imports.gi.St

let _indicator

const WebcamStatusInterface = '<node>\
  <interface name="com.uploadedlobster.WebcamAccessMonitor">\
    <method name="getDeviceState">\
      <arg type="s" direction="in"/>\
      <arg type="i" direction="out"/>\
    </method>\
    <method name="getAllDeviceStates">\
      <arg type="a{si}" direction="out"/>\
    </method>\
    <signal name="stateChanged">\
      <arg type="(si)" direction="out"/>\
    </signal>\
  </interface>\
</node>'
const WebcamStatusDbusProxy = Gio.DBusProxy.makeProxyWrapper(WebcamStatusInterface)

const CameraStatusButton = new Lang.Class({
  Name: 'WebcamAccessMonitor.CameraStatusButton',
  Extends: PanelMenu.Button,

  _init: function () {
    this.parent(0.0, _('Webcam status'))

    const icon = new St.Icon({
      icon_name: 'camera-web-symbolic',
      style_class: 'system-status-icon'
    })
    this.actor.add_child(icon)
    this.actor.add_style_class_name('webcam-access-monitor')

    this.camera_is_on = false

    this._proxy = new WebcamStatusDbusProxy(
      Gio.DBus.session,
      'com.uploadedlobster.WebcamAccessMonitor',
      '/com/uploadedlobster/WebcamAccessMonitor')

    this._setupWatch()
    this._checkCameraIsActive()
  },

  _setupWatch: function () {
    this._changedSignalId = this._proxy.connectSignal(
      'stateChanged', Lang.bind(this, this._onStateChange))
  },

  _onStateChange: function (emitter, senderName, parameters) {
    // parameters is a tuple of type (si), e.g. ('/dev/video0', 1)
    const device = parameters[0][0]
    const state = parameters[0][1]
    log('DEBUG: Camera device ' + device + ' changed state ' + state)
    this._updateCameraStatus(state === 1)
  },

  _checkCameraIsActive: function () {
    this._proxy.getAllDeviceStatesRemote(
      Lang.bind(this, (result, excp) => {
        [result] = result
        let status = true
        for (let device in result) {
          log('DEBUG: Camera device ' + device + ' state ' + result[device])
          status &= result[device] === 1
        }

        this._updateCameraStatus(status)
      }))
  },

  _updateCameraStatus: function (status) {
    if (this.camera_is_on !== status) {
      this.camera_is_on = status

      // if (this.camera_is_on) {
      //   Main.notify("Webcam activated");
      // }
      // else {
      //   Main.notify("Webcam deactivated");
      // }
    }

    this.actor.visible = this.camera_is_on
  }
})

function init () {}

function enable () {
  _indicator = new CameraStatusButton()
  Main.panel.addToStatusArea('camera_button', _indicator)
}

function disable () {
  _indicator.destroy()
}
