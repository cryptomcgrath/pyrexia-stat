import pexpect
import sys
from collections import defaultdict
import threading
import time
import utils as ut
import string

class BleError(Exception):
    pass

class ConnectError(BleError):
    "Error connecting to device"
    pass

class ExpectTimeout(BleError):
    "Timeout expecting response"
    pass

class NoResponseError(BleError):
    "No response received"
    pass

class ValueError(BleError):
    "Invalid value given"
    pass


RESPONSE_WRITE_SUCCESS = "Characteristic value was written successfully\r\n"
RESPONSE_READ_SUCCESS = "Characteristic value/descriptor: "
RESPONSE_CONNECT_SUCCESS = "Connection successful"
RESPONSE_SPAWN_SUCCESS = r'\[LE\]>'

DEFAULT_CONNECT_TIMEOUT=10
TIMEOUT=10

class BleDevice(object):

    def __init__(self, mac, adapter='hci0'):
        """
        Initializes the device
        Args:
            mac (str): The mac address of the device to connect to
            in the format xx:xx:xx:xx:xx:xx

            adapter (str): The adapter interface
        """
        self._mac = mac
        self._handles = {}               # Used for tracking which handles
        self._subscribed_handlers = {}   # have subscribed callbacks
        self._callbacks = defaultdict(set)
        self._gatt = None
        self._connected = False
        self._gatt_lock = threading.RLock()
        self._lock = threading.Lock()

        cmd = "gatttool -b {} -i {} -I".format(self._mac, adapter)
        self._gatt = pexpect.spawn(cmd)
        self._gatt.expect(RESPONSE_SPAWN_SUCCESS, timeout=1)

        self._running = True
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        
    def connect(self, timeout=DEFAULT_CONNECT_TIMEOUT):
        """
        Connects to the device 
        Args:
            timeout (int): The timeout to wait for a connection in seconds
        """
        try:
            self._gatt.sendline("connect")
            self._gatt.expect(RESPONSE_CONNECT_SUCCESS, timeout=timeout)
            self._connected = True
            if not self._running:
                self._thread.run()
        except:
            msg = self._gatt.after
            raise ConnectError(msg)

    def stop(self):
        """
        Disconnects from the device and stops gatttool
        """
        self._running = False
        if self._gatt.isalive():
            self._gatt.sendline('exit')

            # wait one second for gatttool to stop
            for i in range(100):
                if not self._gatt.isalive(): break
                time.sleep(0.01)

            self._gatt.close()
            self._connected = False

    def run(self):
        """Listens for notifications."""
        while self._running:
            with self._gatt_lock:
                try:
                    self._expect('dummy value', timeout=0.1)
                except ExpectTimeout:
                    pass
                except (ConnectError, pexpect.EOF):
                    break

            time.sleep(0.05)  # yield lock 

    def read_hnd(self, hnd):
        """
        Read bluetooth characteristic handle
        Args:
            hnd (str): The handle to read
        """
        if not self._connected:
            msg = "Device not connected"
            raise ConnectError(msg)
        with self._gatt_lock:
            self._gatt.sendline("char-read-hnd "+hnd)
            self._gatt.expect(RESPONSE_READ_SUCCESS, timeout=TIMEOUT)
            self._expect("\r\n", timeout=TIMEOUT)
            hex_str = self._gatt.before.decode().replace(" ","")
            return hex_str

    def write_req(self, hnd, val):
        """
        Write bluetooh characteristic handle
        Args:
            hnd (str): The handle to write to
            val (str): The value to write as a hex string
        Returns:
            True if success, otherwise False
        """
        try:
            self._gatt.sendline("char-write-req "+hnd+" "+val)
            self._expect(RESPONSE_WRITE_SUCCESS, timeout=TIMEOUT)
        except ExpectTimeout:
            msg="No response from write_req"
            raise NoResponseError(msg)

    def _expect(self, expected, timeout=DEFAULT_CONNECT_TIMEOUT):
        with self._gatt_lock:
            patterns = [
                expected,
                'Notification handle = .*? \r',
                'Indication   handle = .*? \r',
                '.*Invalid file descriptor.*',
                '.*Disconnected\r'
            ]
            while True:
                try:
                    matched_pattern_index = self._gatt.expect(patterns, timeout)
                    if matched_pattern_index == 0:
                        break
                    elif matched_pattern_index in {1, 2}:
                        self._handle_notification(self._gatt.after)
                    elif matched_pattern_index in {3, 4}:
                        msg = ''
                        if self._running:
                            msg = 'unexpectedly disconnected'
                            self._running = False
                        raise ConnectError(msg)
                except pexpect.TIMEOUT:
                    msg = 'timed out waiting for a response'
                    raise ExpectTimeout(msg)

    def _handle_notification(self, msg):
        """Handle a notification.

        Propagates the handle and value to all registered callbacks.

        Args:
            msg (str): The notification message, which looks like these:

                    Notification handle = <handle> value: <value> 
                    Indication   handle = <handle> value: <value>
        """
        print("handle_notfication msg={}".format(msg))
        hex_handle_b, _, hex_value_b = msg.split(b' ', maxsplit=5)[3:]
        hex_handle = hex_handle_b.decode("utf-8").replace("0x","")
        hex_value = hex_value_b.decode("utf-8")
        print("handle={} value={}".format(hex_handle, hex_value))


        handle = int(hex_handle, 16)
        value = bytearray.fromhex(hex_value)

        with self._lock:
            if hex_handle in self._callbacks:
                for callback in self._callbacks[hex_handle]:
                    callback(hex_handle, hex_value)

    def subscribe(self, handle, control_handle, callback=None, mode=0):
        """Subscribes to notification/indiciatons from a characteristic.

        This is achieved by writing to the control handle, which is assumed
        to be `handle`+1. If indications are requested and we are already
        subscribed to notifications (or vice versa), we write 0300 
        (signifying we want to enable both). Otherwise, we write 0100 for
        notifications or 0200 for indications.

        Args:
            handle (str): The handle to listen for as a hex string
            callback (f(int, bytearray)): A function that will be called
                when the notif/indication is received. When called, it will be
                passed the handle and value.
            mode (int): If 0, requests notifications. If 1, requests 
                indications. If 2, requests both. Any other value will
                result in a ValueError being raised. 

        Raises:
            ExpectTimeout: If writing to the control handle fails.
            ValueError: If `mode` is not in {0, 1, 2}.
        """
        if mode not in {0, 1, 2}:
            message = ('mode must be 0 (notifications), 1 (indications), or'
                       '2 (both).')
            raise ValueError(message)

        this, other = \
                ("0100", "0200") if mode == 0 else \
                ("0200", "0100") if mode == 1 else \
                ("0300", "0300")
        both = "0300"

        handle = handle.replace("0x","")

        with self._lock:
            if callback is not None:
                self._callbacks[handle].add(callback)

            previous = self._subscribed_handlers.get(handle, None)
            if not previous in [this, both]:
                value = both if previous == other else this
                print("writing value {} to handle {}".format(value, control_handle))
                self.write_req(control_handle, value)
                self._subscribed_handlers[handle] = value

    def unsubscribe(self, handle, control_handle, callback=None):
        """Unsubscribes from notif/indications on a handle.

        Writes 0000 to the control handle, which is assumed to be `handle`+1.
        If `callback` is supplied, removes `callback` from the list of
        callbacks for this handle.

        Args:
            handle (int): The handle to unsubscribe from.
            callback (f(int, bytearray)): The callback to remove,
                previously passed as the `callback` parameter of
                self.subscribe(handle, callback).

        Raises:
            ExpectTimeout: If writing to the control handle fails.
        """
        value = "0000"
        with self._lock:
            if callback is not None:
                self._callbacks[handle].remove(callback)

            if self._subscribed_handlers.get(handle, None) != value:
                self.write_req(control_handle, value)
                self._subscribed_handlers[handle] = value 


