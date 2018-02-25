import logging
import time
import uuid
import binascii
import Adafruit_BluefruitLE

# Enable debug output.
#logging.basicConfig(level=logging.DEBUG)

SBOT_SERVICE_UUID = uuid.UUID('CBA20D00-224D-11E6-9FB8-0002A5D5C51B')
SBOT_NOTIFY_UUID  = uuid.UUID('CBA20003-224D-11E6-9FB8-0002A5D5C51B')
SBOT_WRITE_UUID   = uuid.UUID('CBA20002-224D-11E6-9FB8-0002A5D5C51B')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    # print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected devices.  Good for cleaning up and
    # starting from a fresh state.
    # print('Disconnecting any connected devices...')
    ble.disconnect_devices([SBOT_SERVICE_UUID])

    # Scan for devices.
    # print('Searching for devices...')
    try:
        adapter.start_scan()
        # Search for the first device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).


        print('Press Ctl-C to stop...\n')

        known_bots = set()
        while True:
            print('Searching...')
            # Call UART.find_devices to get a list of any UART devices that
            # have been found.  This call will quickly return results and does
            # not wait for devices to appear.
            found = set(ble.find_devices(service_uuids=[SBOT_SERVICE_UUID]))
            # Check for new devices that haven't been seen yet and print out
            # their name and ID (MAC address on Linux, GUID on OSX).
            new = found - known_bots
            for device in new:
                print('Found bot: {0} [{1}]'.format(device.name, device.id))
                known_bots.update(new)
            # Sleep for a second and see if new devices have appeared.
            time.sleep(1.0)

    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

   

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)


