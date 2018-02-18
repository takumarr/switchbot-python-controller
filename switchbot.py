import sys
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

SBOT_PRESS_CMD = binascii.unhexlify('570100')
SBOT_TURNON_CMD = binascii.unhexlify('570101')
SBOT_TURNOFF_CMD = binascii.unhexlify('570102')

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
    #print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected devices.  Good for cleaning up and
    # starting from a fresh state.
    #print('Disconnecting any connected devices...')
    ble.disconnect_devices([SBOT_SERVICE_UUID])

    # Scan for devices.
    print('Searching for device...')
    try:
        adapter.start_scan()
        # Search for the first device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        d = ble.find_device(service_uuids=[SBOT_SERVICE_UUID])
        if d is None:
            raise RuntimeError('Failed to find device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    devices = ble.find_devices(service_uuids=[SBOT_SERVICE_UUID])
    #print('devices count=' + str(len(devices)))
    assert len(devices) > 0, "No device!"

    tmp = filter(lambda n:str(n.id) == bot_id, devices)
    if len(tmp) == 0:
        print(bot_id + ' is not found.')
        return

    device = tmp[0]

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for at least the specified
        # service and characteristic UUID lists.  Will time out after 60 seconds
        # (specify timeout_sec parameter to override).
        print('Discovering services...')
        device.discover([SBOT_SERVICE_UUID], [SBOT_NOTIFY_UUID, SBOT_WRITE_UUID])

        # Find the service and its characteristics.
        serv = device.find_service(SBOT_SERVICE_UUID)
        #print('Serv:' + str(serv.uuid))
        notify = serv.find_characteristic(SBOT_NOTIFY_UUID)
        write = serv.find_characteristic(SBOT_WRITE_UUID)

        '''
        if not notify is None:
            print('Notify:' + str(notify.uuid))

        if not notify is None:
            print('Write :' + str(write.uuid))
        '''

        # Write a string to the TX characteristic.
        print('Sending message to device...')
        write.write_value(bot_cmd)

        # Function to receive RX characteristic changes.  Note that this will
        # be called on a different thread so be careful to make sure state that
        # the function changes is thread safe.  Use queue or other thread-safe
        # primitives to send data to other threads.
        #def received(data):
        #    print('Received: {0}'.format(data))

        # Turn on notification of RX characteristics using the callback above.
        #print('Subscribing to RX characteristic changes...')
        #rx.start_notify(received)

        # Now just wait for 30 seconds to receive data.
        print('Waiting a few seconds to receive data from the device...')
        time.sleep(1)
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()

argvs = sys.argv
argc = len(argvs)

if not argc is 3:
    print('Usage: # python %s switchbot_ID [press | on | off]' % argvs[0])
    print('\nPlease use search_switchbot.py to check your switchbot_ID.')
    quit()

bot_id = argvs[1]
cmd  = argvs[2]

if cmd == 'on':
    bot_cmd = SBOT_TURNON_CMD
elif cmd == 'off':
    bot_cmd = SBOT_TURNOFF_CMD
elif cmd == 'press':
    bot_cmd = SBOT_PRESS_CMD
else:
    print('Usage: # python %s switchbot_ID [press | on | off]' % argvs[0])
    print('\nPlease use search_switchbot.py to check your switchbot_ID.')
    quit()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)


