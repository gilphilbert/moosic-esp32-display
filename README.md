# moosic-esp32-display
A display driver for a small OLED display attached to an ESP32.

## Hardware
An ESP32 based dev board
A small OLED driven by an ssd1306 (i2c)
* four wire, including power

### Installation
* Make sure your device is running the latest MicroPython code
* Install adafruit-ampy `pip3 install adafruit-ampy`
```
git clone https://github.com/gilphilbert/moosic-esp32-display.git
cd moosic-esp32-display.git
ampy put *
ampy run main.py
```
