
const St = imports.gi.St;
const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;
const Lang = imports.lang;

let _indicator;

function CameraStatusButton() {
    this._init();
}

CameraStatusButton.prototype = {
    __proto__: PanelMenu.SystemStatusButton.prototype,

    _init: function() {
        PanelMenu.SystemStatusButton.prototype._init.call(this, 'camera-web-symbolic');

        this.camera_device = '/dev/video0';
        this.camera_file = Gio.file_new_for_uri('file://' + this.camera_device);
	this.camera_is_on = false;

        this._onStatusChange();
        this._setupWatch();
    },

    _setupWatch: function() {
	// Unfortunately FileMonitor does not monitor the inotify
	// IN_OPEN and IN_CLOSE_NOWRITE events, so we miss some events.
	// As there is no direct access to inotify there probably
	// needs to be some kind of daemon we communicate to via DBUS.
	// Cameramonitor could be extended, see
	// https://code.launchpad.net/~cameramonitor-team/cameramonitor/
	
        this.monitor = this.camera_file.monitor_file(
	    Gio.FileMonitorFlags.NONE, null);
        this.monitor.connect('changed', Lang.bind(this, this._onStatusChange));
    },

    _onStatusChange: function() {
	log('DEBUG: Camera device ' + this.camera_device + ' changed.');
	this._checkCameraIsActive(Lang.bind(this, this._checkCameraCallback));
    },

    _checkCameraIsActive: function(callback) {
	try {
	    var info = this.camera_file.query_info(
		'access::*',
		Gio.FileQueryInfoFlags.NONE,
		null);

	    if (!info.get_attribute_boolean('access::can-read')) {
		log('WARNING: No read access to ' + this.camera_device);
		callback(false);
		return;
	    }
	}
	catch (e) {
	    log('WARNING: Cannot access device ' + this.camera_device);
	    log(e);
	    callback(false);
	    return;
	}

	let [success, pid] = GLib.spawn_async(
	    null,
	    ['fuser', '-s', this.camera_device],
	    null,
	    GLib.SpawnFlags.SEARCH_PATH | GLib.SpawnFlags.DO_NOT_REAP_CHILD,
	    null);

	GLib.child_watch_add(GLib.PRIORITY_DEFAULT, pid, function(pid, status) {
            GLib.spawn_close_pid(pid);
            log("DEBUG: Camera status=" + status);
	    callback(status == 0);
 	});
    },

    _checkCameraCallback: function(status) {
	if (this.camera_is_on != status) {
	    this.camera_is_on = status;

	    // if (this.camera_is_on) {
	    // 	Main.notify("Webcam activated");
	    // }
	    // else {
	    // 	Main.notify("Webcam deactivated");
	    // }
	}
	
	this.actor.visible = this.camera_is_on;
    },
};

function init() {
}

function enable() {
    _indicator = new CameraStatusButton;
    Main.panel.addToStatusArea('camera_button', _indicator);
}

function disable() {
    _indicator.destroy();
}
