#include <Adafruit_NeoPixel.h>
#include <TinyWire.h>

#define PIN            3  // Define the pin to which the data line of the NeoPixel strip is connected
#define NUMPIXELS      8  // Define the number of pixels in your LED strip

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();  // Initialize all pixels to 'off'

  TinyWire.begin(0x27);  // Set I2C address to 4
  TinyWire.onReceive(receiveEvent);
}

void loop() {
  // Your main loop code here
}

void receiveEvent() {
  // Receive 4 bytes over I2C
  uint8_t index = TinyWire.receive();

  while(TinyWire.available() >= 3 and index < NUMPIXELS) {
    uint8_t red = TinyWire.receive();
    uint8_t green = TinyWire.receive();
    uint8_t blue = TinyWire.receive();
    strip.setPixelColor(index, strip.Color(red, green, blue));
    index++;
  }

  strip.show();
}


