###############################################################
#
# AQM1248A class for MicroPython 
#
# Copyright(c) 2017-2018 forester3
# This software is released under the MIT License, see LICENSE
#
###############################################################

from machine import Pin, SPI
from time import sleep_ms
from fonts import font

class ChrLcd:
    pins = {}

    # limits

    MAX_COL = const(127)
    MAX_PAGE = const(7)
    MAX_LINE = const((MAX_PAGE+1)*8-1)

    # instance variables

    page = 0
    col  = 0
    start_line = 0
    scrl_line  = 8
    scroll = False

    def lcd_cmd(self, cmd ):
        self.pins['LCD_CS'].off()
        self.pins['LCD_RS'].off()
        self.SPI.write(cmd)
        self.pins['LCD_CS'].on()

    def lcd_data(self, data ):
        self.pins['LCD_CS'].off()
        self.pins['LCD_RS'].on()
        self.SPI.write(data)
        self.pins['LCD_RS'].off()
        self.pins['LCD_CS'].on()

    def set_contrast(self, a, b):
        if a < 0:
            a = 0
        elif a > 3:
            a = 3
        self.lcd_cmd( bytearray([0x20 | a ]) )
        self.lcd_cmd( b'\x81' )
        if b < 0:
            b = 0
        elif b > 0x3F:
            b = 0x3F
        self.lcd_cmd( bytearray([b]) )

    def show(self, x):
        if x:
            self.lcd_cmd(b'\xAF')
        else:
            self.lcd_cmd(b'\xAE')

    def reverse(self, x):
        if x:
            self.lcd_cmd(b'\xA7')
        else:
            self.lcd_cmd(b'\xA6')

    def all_on(self, x):
        if x:
            self.lcd_cmd(b'\xA5')
        else:
            self.lcd_cmd(b'\xA4')

    def set_page(self, p):
        if p < 0:
            p = 0
        elif p > MAX_PAGE-2:
            p = MAX_PAGE-2
        self.page = p
        self.lcd_cmd( bytearray([0xb0 + p]) )

    def set_col(self, c):
        if c < 0:
            c = 0
        elif c > MAX_COL:
            c = MAX_COL
        self.col = c
        self.lcd_cmd( bytearray([0x10 + (c >> 4)]) )
        self.lcd_cmd( bytearray([0x00 + (c & 0x0f)]) )

    def set_start_line(self, start):
        if start < 0:
            start = 0
        elif start > MAX_LINE:
            start = MAX_LINE
        self.start_line = start
        self.lcd_cmd(bytearray([0x40 | start]))

    def add_col(self, x):
        self.col += x
        if self.col > MAX_COL:
            self.add_page(self.col //(MAX_COL+1))
            self.col %= (MAX_COL+1)
            self.set_col(self.col)
        elif self.col < 0:
            self.col = 0
            self.set_col(0)

    def add_page(self, x):
        self.page += x
        if self.page > MAX_PAGE:
            self.page %= (MAX_PAGE+1)

        self.set_page(self.page)
        self.clear_page()

        if self.page == (self.start_line//(MAX_PAGE+1)+(MAX_PAGE-1)) % (MAX_PAGE+1):
            self.start_line += self.scrl_line * x
            self.scroll = True
            if self.start_line > MAX_LINE:
                self.start_line %= (MAX_LINE+1)
            self.set_start_line( self.start_line )

    def put_char(self, h: int, color=1):
        if h == 0x0A:
            self.add_page(1)
            self.set_col(0)
        elif h >= 0x20 and h <= 0xdf:
            if self.col+len(font[h-0x20])+1 > MAX_COL:
                self.add_page(1)
                self.set_col(0)

            if color:
                self.lcd_data( font[h-0x20] )
                self.lcd_data( b'\x00' )
            else:
                for x in range(len(font[h-0x20])):
                    self.lcd_data( bytearray([~font[h-0x20][x]]))
                self.lcd_data( b'\xFF' )
                   
            self.add_col( len(font[h-0x20])+1 )
        else:
            raise ValueError('ChrLcd.put_char(h): value is not 0x0A,0x20to0xDF.')

    def write(self, string, color=1):
        for c in string:
            c = ord(c)
            self.put_char(c, color)                

    def text(self, string, x, y, color=1):
        if y < 0:
            y = 0
        elif y > MAX_PAGE:
            y = MAX_PAGE

        y += self.start_line//8

        if y > MAX_PAGE:
            y %= (MAX_PAGE+1)
        self.scroll = False
        self.set_page(y)
        self.set_col(x)

        for c in string:
            c = ord(c)
            self.put_char(c, color)

    def clear_page(self):
        self.set_col(0)
        for c in range(0, MAX_COL, 6):
            self.lcd_data( b'\x00\x00\x00\x00\x00\x00' )
           
    def fill(self, x):
        for p in range(MAX_PAGE):
            self.set_page(p)
            self.set_col(0)
            for c in range(0, MAX_COL, 6):
                if x:
                    self.lcd_data( b'\xff\xff\xff\xff\xff\xff' )
                else:
                    self.lcd_data( b'\x00\x00\x00\x00\x00\x00' )
        self.set_page(0)
        self.set_col(0)
        self.scroll = False
        self.set_start_line(0)

    def clear(self):
        self.fill(0)
        
    def __init__(self, SPIn, cs_pin, rs_pin):
        self.pins['LCD_CS'] = Pin(cs_pin, Pin.OUT)
        self.pins['LCD_RS'] = Pin(rs_pin, Pin.OUT)

        self.pins['LCD_CS'].on()
        self.pins['LCD_RS'].on()

        self.SPI = SPIn
        self.SPI.init( baudrate=20000000, polarity=1, phase=1 )

        self.show(0)
                
        self.lcd_cmd( b'\xA0\xC8\xA3' )

        self.lcd_cmd(b'\x2C')                   # internal regulator
        sleep_ms(2)
        self.lcd_cmd(b'\x2E')
        sleep_ms(2)
        self.lcd_cmd(b'\x2F')

        self.set_contrast(3, 0x1c)
        self.all_on(0)
        self.reverse(0)
        self.show(1)

