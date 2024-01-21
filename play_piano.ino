#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <stdint.h>

#define I2C_ADDR 0x08

#define MAX_KEYS_PER_TRANSFER 10
#define LED_PIN 1
#define NUM_LEDS 4

struct LedInfo {
  uint8_t ledIdx;
  uint8_t red;
  uint8_t green;
  uint8_t blue;
  uint16_t delayMs;
};

Adafruit_NeoPixel led_strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setLEDs(struct LedInfo* ledInfo, int numLedInfo) {
  for (int i = 0; i < numLedInfo; i++) {
    // todo figure out actual conversion for ledidx
    for (int j = 0; j < 4; j++) {
      led_strip.setPixelColor(ledInfo[i].ledIdx + j, led_strip.Color(ledInfo[i].red, ledInfo[i].green, ledInfo[i].blue));
      led_strip.show();
      delay(ledInfo[i].delayMs);
    }
  }
}

void i2cRecvCallback(int numBytes) {
  struct LedInfo led_info[MAX_KEYS_PER_TRANSFER];
  uint8_t num_led_info = numBytes / sizeof(struct LedInfo);
  int extra_bytes = numBytes % sizeof(struct LedInfo);
  if (extra_bytes != 0) {
    Serial.print(extra_bytes);
    Serial.print(" extra bytes");
    Serial.println();
  }

  uint16_t delay_temp;
  for (int i = 0; i < num_led_info; i++) {
    led_info[i].ledIdx = Wire.read();
    led_info[i].red = Wire.read();
    led_info[i].green = Wire.read();
    led_info[i].blue = Wire.read();
    delay_temp = Wire.read();
    delay_temp = delay_temp << 8;
    delay_temp += Wire.read();
    led_info[i].delayMs = delay_temp;
  }
}

void setup() {
  Wire.begin(I2C_ADDR);
  Wire.onReceive(i2cRecvCallback);
  led_strip.begin();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
}
