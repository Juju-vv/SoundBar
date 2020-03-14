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
Then install [Pyaudio](https://github.com/intxcc/pyaudio_portaudio)

###### Python 
If pip is not installed you should get it by downloading [this](https://bootstrap.pypa.io/get-pip.py).
Then in Cygwin go to the directory where you downloaded **get-pip.py** and enter the following command: `pythonX get-pip.py` where 'X' is your python version.  

To run the python script you may have to install 
- Pyserial
- Numpy
- Colour

Simply use `pip install [package name]`

### Arduino



