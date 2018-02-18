# SwitchBot Python Controller
This is library to control your Switch Bots with python on mac.

## Environment
mac Sierra
python 2.7

Bots with password are not supported.

## Installtion
Install　"BluefruitLE".
https://github.com/adafruit/Adafruit_Python_BluefruitLE

```
brew install python

pip2 install pexpect

git clone https://github.com/adafruit/Adafruit_Python_BluefruitLE.git
cd Adafruit_Python_BluefruitLE

python2 setup.py install

# If you dont have objc library
pip2 install -U pyobjc
```

## How to use

Find your Switch Bot ID.

```
$ python2 search_switchbot.py
=== SwitchBot IDs ===
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (None)
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (WoHand)
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (WoHand)
=====================
```

Send a message to your ID.
```
$ python2 switchbot.py xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx press
$ python2 switchbot.py xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx on
$ python2 switchbot.py xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx off
```


## Special Thanks to

Adafruit_Python_BluefruitLE
https://github.com/adafruit/Adafruit_Python_BluefruitLE

OpenWonderLabs/python-host
https://github.com/OpenWonderLabs/python-host

