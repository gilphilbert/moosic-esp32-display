#import network
from machine import Pin, I2C
from time import sleep
import ssd1306
from fonts.font_6x10 import font

# ESP32 Pin assignment 
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def showState(state, title, artist, perc):
    oled.fill(0)
    if state == "pause":
        pause()
    elif state == "play":
        play()
    text(title.encode(), -1, 11)
    text(artist.encode(), 12, 0)
    progress(perc)
    oled.pixel(0, 36, 1)
    oled.show()

def pause():
  for x in range(0, 2):
     for y in range(0, 7):
         oled.pixel(x, y, 1)
  for x in range(4, 6):
     for y in range(0, 7):
         oled.pixel(x, y, 1)

def play():
    for x in range(0, 7):
         oled.pixel(0, x, 1)
    for y in range(1, 5):
        for x in range(0, y):
            oled.pixel(x, y-1, 1)
    for x in range(1, 5):
        for y in range(4, 7-x):
            oled.pixel(x, y, 1)

def text(message, y, x):
    def _plotter(x, y):
        oled.pixel(x, y, 1)
    font.draw_para(message, _plotter, x, y, font.height)

def progress(percent):
    for y in range(25,32):
        oled.pixel(0, y, 1)
        oled.pixel(127, y, 1)
    oled.pixel(1, 25, 1)
    oled.pixel(1, 31, 1)
    oled.pixel(126, 25, 1)
    oled.pixel(126, 31, 1)

    xmax = round(((oled_width - 6) / 100) * percent)

    for x in range(3, xmax):
        for y in range(26, 31):
            oled.pixel(x, y, 1)
