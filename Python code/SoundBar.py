import pyaudio, os, serial, struct
import numpy as np
from time import sleep
from colour import Color
 
port = '/dev/com5'

 
ard = serial.Serial(port,115200,timeout = 1)
num_leds = 144                                                                  # number of LEDS in your strip
 
defaultframes = 512
maxValue = 2**16
peakL = 0
peakR = 0
last_peakL = peakL
last_peakR = peakR
multiplier = 2.25                                                                # you can play with this if you want more of the bar to light up
oldrL = 255
 
#red = Color("hotpink")
#blue = Color("darkblue")
red = Color("red")
blue = Color("purple")
spec_colors = list(blue.range_to(red,int(num_leds/2)))                        # get the gradients

spec_colors_rgbL = []
spec_colors_rgbR = []
spec_colors_rgb = []

for spec_color in spec_colors:                                                  # convert the [0-255] for arduino
    color_array = spec_color.rgb
    spec_colors_rgb.append([int(x * 255) for x in color_array])

for spec_color in spec_colors:                                                  # convert the [0-255] for arduino
    color_array = spec_color.rgb
    spec_colors_rgbL.append([int(x * 255) for x in color_array])

for spec_color in spec_colors:                                                  # convert the [0-255] for arduino
    color_array = spec_color.rgb
    spec_colors_rgbR.append([int(x * 255) for x in color_array])
     
class textcolors:                                                               # this class is only used for the prompt of audio device
    if not os.name == 'nt':
        blue = '\033[94m'
        green = '\033[92m'
        warning = '\033[93m'
        fail = '\033[91m'
        end = '\033[0m'
    else:
        blue = ''
        green = ''
        warning = ''
        fail = ''
        end = ''
 
#Use module
p = pyaudio.PyAudio()                                                           # https://github.com/intxcc/pyaudio_portaudio
 
try:
    default_device_index = p.get_default_input_device_info()                    #Set default to first in list or ask Windows
except IOError:
    default_device_index = -1
 
print (textcolors.blue + "Available devices:\n" + textcolors.end)               #Select Device
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print (textcolors.green + str(info["index"]) + textcolors.end + \
    ": \t %s \n \t %s \n" % (info["name"], \
    p.get_host_api_info_by_index(info["hostApi"])["name"]))
 
    if default_device_index == -1:
        default_device_index = info["index"]
 
if default_device_index == -1:                                                  #Handle no devices available
    print (textcolors.fail + "No device available. Quitting." + textcolors.end)
    exit()
 
device_id = int(input("Choose device [" + textcolors.blue + \
    str(default_device_index) + textcolors.end + "]: ") or default_device_index)#Get input or default
print ("")
 
try:
    device_info = p.get_device_info_by_index(device_id)                         #Get device info
except IOError:
    device_info = p.get_device_info_by_index(default_device_index)
    print (textcolors.warning + "Selection not available, using default." + \
        textcolors.end)
 
is_input = device_info["maxInputChannels"] > 0                                  #Choose between loopback or standard mode
is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    print (textcolors.blue + "Selection is input using standard mode.\n" + \
        textcolors.end)
else:
    if is_wasapi:
        useloopback = True;
        print (textcolors.green + \
            "Selection is output. Using loopback mode.\n" + textcolors.end)
    else:
        print (textcolors.fail + \
            "Selection is input and does not support " + \
            "loopback mode. Quitting.\n" + textcolors.end)
        exit()
 
if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]):        #Open stream
    channelcount = device_info["maxInputChannels"]
else:
    channelcount = device_info["maxOutputChannels"]
 
stream = p.open(format = pyaudio.paInt16,
                channels = channelcount,
                rate = int(device_info["defaultSampleRate"]),
                input = True,
                frames_per_buffer = defaultframes,
                input_device_index = device_info["index"],
                as_loopback = useloopback)
 
while True:
    try:
        data = np.frombuffer(stream.read(1024),dtype=np.int16)                  # read from buffer
        dataL = data[0::2]
        dataR = data[1::2]
        peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue                    # get max value for the left channel
        peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue                    # get max value for the right channel
        bar_array = [[0,0,0]] * num_leds                                        # initialize an array for all of the LEDS on the off position
 
        
        

        to_fill_LAnim = int(min(num_leds / 2 * peakL * multiplier, num_leds/2))
        to_fill_RAnim = int(min(num_leds / 2 * peakR * multiplier, num_leds/2))    # how many LEDs are we going to fill up for the left channel


        if to_fill_LAnim < int(0.4 * num_leds / 2) or to_fill_RAnim < int(0.4 * num_leds / 2):
            to_fill_L = int(min(num_leds  * peakL * multiplier , num_leds))     # how many LEDs are we going to fill up for the left channel
            to_fill_R = int(min(num_leds  * peakR * multiplier , num_leds))     # how many LEDs are we going to fill up for the right channel

            

            to_Fillmin = 30

            if to_fill_L + 20 > 255:
                to_fill_L = 255
            else:
                to_fill_L = to_fill_L + 30

                if  to_fill_L > 30 :
                    to_fill_LR =  int(np.random.randint(to_Fillmin,to_fill_L, size=1)[0])
                    to_fill_LG =  int(np.random.randint(to_Fillmin,to_fill_L, size=1)[0])
                    to_fill_LB =  int(np.random.randint(to_Fillmin,to_fill_L, size=1)[0])
                else:
                    to_fill_LR =  0
                    to_fill_LG =  0
                    to_fill_LB =  0                
            if(to_fill_L < 0) :
                to_fill_L = 0

            if to_fill_R + 20 > 255:
                to_fill_R = 255
            else:
                to_fill_R = to_fill_R + 30

                if  to_fill_R > 30 :
                    to_fill_RR =  int(np.random.randint(to_Fillmin,to_fill_R, size=1)[0])
                    to_fill_RG =  int(np.random.randint(to_Fillmin,to_fill_R, size=1)[0])
                    to_fill_RB =  int(np.random.randint(to_Fillmin,to_fill_R, size=1)[0])
                else:
                    to_fill_RR =  0
                    to_fill_RG =  0
                    to_fill_RB =  0                
            if(to_fill_R < 0) :
                to_fill_R = 0
                
            randDiv = np.random.randint(100, 256, size=1)[0]
            


            for i in reversed(range(0, int(num_leds/2))):            
                spec_colors_rgbL[i][0] =int(to_fill_LR -(to_fill_LR*randDiv/256))
                spec_colors_rgbL[i][1] = int(to_fill_LG -(to_fill_LG*randDiv/256))
                spec_colors_rgbL[i][2] = int(to_fill_LB -(to_fill_LB*1/256))
                
                bar_array[int(num_leds/2)-i] = spec_colors_rgbL[i]                                # color them based on the spectrum we generated earlier

            for i in range(0, int(num_leds/2)):
                spec_colors_rgbR[i][0] =int(to_fill_RR -(to_fill_RR*randDiv/256))
                spec_colors_rgbR[i][1] = int(to_fill_RG -(to_fill_RG*randDiv/256))
                spec_colors_rgbR[i][2] = int(to_fill_RB -(to_fill_RB*1/256))
                pos = int(num_leds/2) + i                                               # turn them on right to left
                bar_array[pos] = spec_colors_rgbR[i]                                 # color them based on the spectrum we generated earlier

        else:

            for i in reversed(range(0, to_fill_LAnim)):
                bar_array[int(num_leds/2)-i] = spec_colors_rgb[i]                                   # color them based on the spectrum we generated earlier
    
            
            for i in reversed(range(0, to_fill_RAnim)):
                pos = int(num_leds/2) + i                                               # turn them on right to left
                bar_array[pos] = spec_colors_rgb[i]                                 # color them based on the spectrum we generated earlier

            ### The following is to make the peak the color red and to persist it
            last_peakL = last_peakL - 1                                             # move the red led further down for a "falling" effect
            last_peakR = last_peakR - 1                                             # move the red led further down for a "falling" effect

            if  last_peakL <= to_fill_LAnim:                                             # if the red LED is less than the peak:
                last_peakL = to_fill_LAnim                                              # make the red move up to the new peak
            if last_peakR <= to_fill_RAnim:
               last_peakR = to_fill_RAnim

            
            

     
            ### after how many percent of the bar do we want to start drawing the Red LED
            if last_peakL > int(0.25 * num_leds / 2):
                bar_array[int(num_leds/2)-last_peakL] = [245,245,245]
            if last_peakR > int(0.25 * num_leds / 2):
                bar_array[int(num_leds/2) + last_peakR-1] = [245,245,245]
        
        result = False;
        if len(bar_array) > 0 :
            result = bar_array.count(bar_array[0]) == len(bar_array)

        

        ## send to arduino
        for i in range(0,num_leds):
            ard.write(b'L') # 'L'                                               # the arduino is expecting an L to begin receiving LED info
            ard.write(bytes([i,bar_array[i][0],bar_array[i][1],bar_array[i][2]])) # send the LED info in byte form
        ard.write(b'Z') # 'Z'                                                   # tell it to draw the LEDs
        ard.flushInput()                                                        # don't know why, but without this, it does not work.
        ard.flush()                                                             # don't know why, but without this, it does not work.
    except Exception as e:
        print(e)
        if e == 'Write timeout':                                                # if we timeout, attempt to open the connection again
            print("restarting connection")
            ard.close()
            ard.open()
    sleep(0.005)      