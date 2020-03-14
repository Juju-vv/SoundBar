#include "FastLED.h"
#include "Ramp.h"

#define NUM_LEDS 144
CRGB leds[NUM_LEDS];

#define PIN 6
#define MAX_DELAY 65
#define RED_MAX 255
#define GREEN_MAX 255
#define BLUE_MAX 255

rampFloat myRamp;
rampInt myRedRamp;
rampInt myGreenRamp;
rampInt myBlueRamp;

 
 
void setup() {

  delay(1000);
    // initialize serial
  Serial.begin(115200);
  FastLED.addLeds<WS2811, PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(15);
  FastLED.show(); // Initialize all pixels to 'off'

  myRamp.go(MAX_DELAY);
  myRamp.go(1.5,5000,QUINTIC_INOUT,FORTHANDBACK);
  
}
 
void loop() {
   while (Serial.available() > 0) {
        uint8_t serial = Serial.read();
        if (serial == 'Z') {
            showStrip();
        }
        else if (serial == 'L') {
            int i = getNextInput();
            int r = getNextInput();
            int g = getNextInput();
            int b = getNextInput();
            setPixel(i,r,g,b);
        }
   Serial.flush();
  }
 
}
 
uint8_t getNextInput() {
  while(!Serial.available()); // wait for a character
  return Serial.read();
}

void showStrip() {
 #ifdef ADAFRUIT_NEOPIXEL_H
   // NeoPixel
   strip.show();
 #endif
 #ifndef ADAFRUIT_NEOPIXEL_H
   // FastLED
   FastLED.show();
 #endif
}

void setPixel(int Pixel, byte red, byte green, byte blue) {
 #ifdef ADAFRUIT_NEOPIXEL_H
   // NeoPixel
   strip.setPixelColor(Pixel, strip.Color(red, green, blue));
 #endif
 #ifndef ADAFRUIT_NEOPIXEL_H
   // FastLED
   leds[Pixel].r = red;
   leds[Pixel].g = green;
   leds[Pixel].b = blue;
 #endif
}

void setAll(byte red, byte green, byte blue) {
  for(int i = 0; i < NUM_LEDS; i++ ) {
    setPixel(i, red, green, blue);
  }
  showStrip();
}
