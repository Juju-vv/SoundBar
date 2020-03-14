# SoundBar
Sound reactive LED strip using Python and Arduino. 

Inspired by https://robtrevino.com/2019/06/23/using-a-rgb-led-strip-as-an-audio-visualizer/. I took his code and made my own version of it, it is not perfect but it works. So feel free to play with it and improve it !

## What you'll need
- Arduino and Arduino IDE
- LED Strip compatible with Arduino's FastLED/Neopixel library (I'm using Adafruit Neopixel 144 LEDS - 1m LED Strip)
- Cygwin with developper tools and python (You can use Microsoft Visual Studio but i haven't tried)
- Pyaudio with Portaudio https://github.com/intxcc/pyaudio_portaudio

## Installing 

###### Cygwin
You first need to install Cygwin with the basic developper tools and also Python (I'm using Python version 3.6.9)
Then install [**Pyaudio**](https://github.com/intxcc/pyaudio_portaudio)

###### Python 
If pip is not installed you should get it by downloading [**this**](https://bootstrap.pypa.io/get-pip.py).
Then in Cygwin go to the directory where you downloaded **get-pip.py** and enter the following command: `pythonX get-pip.py` _where 'X' is your python version._ 

To run the python script you may have to install 
- Pyserial
- Numpy
- Colour

Simply use `pip install [package name]`

## Using

#### Arduino circuit

See this [**link**](https://www.tweaking4all.com/wp-content/uploads/2014/01/arduino_usb_and_extrenal_power_ws2812-800x380.jpg) to wire the LED strip to your Arduino

The Arduino code is using PIN 6 to command the LED strip.

#### Python script
Cygwin is showing serial port as `dev\ttySX` where is `X` is the COM port of your Arduino with an offset of 1. 

So for example if your Arduino is using COM3, go to the python script line 6 and change it to
``` python
port = '\dev\ttyS2' 
```
You can also use ***\dev\com3***

#### Final step
Plug in your Arduino with the code on it then run the python script. It will ask you to select a device, select the device you use for the sound and you're done ! Enjoy !

# Note

With Cygwin there's an issue where you will have to first open the Serial monitor in Arduino IDE when Arduino is plugged in for the first time and then run the script. Otherwise it will not be able to connect to the serial port. 



