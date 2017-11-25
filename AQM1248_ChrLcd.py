###############################################################
#
# AQM1248A class for MicroPython 
#
# Copyright(c) 2017 forester3
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

    def lcdCmd(self, cmd ):
        self.pins['LCD_CS'].off()
        self.pins['LCD_RS'].off()
        self.SPI.write(cmd)
        self.pins['LCD_CS'].on()

    def lcdData(self, data ):
        self.pins['LCD_CS'].off()
        self.pins['LCD_RS'].on()
        self.SPI.write(data)
        self.pins['LCD_RS'].off()
        self.pins['LCD_CS'].on()

    def setContrast(self, a, b):
        if a < 0:
            a = 0
        elif a > 3:
            a = 3
        self.lcdCmd( bytearray([0x20 | a ]) )
        self.lcdCmd( b'\x81' )
        if b < 0:
            b = 0
        elif b > 0x3F:
            b = 0x3F
        self.lcdCmd( bytearray([b]) )

    def show(self, x):
        if x:
            self.lcdCmd(b'\xAF')
        else:
            self.lcdCmd(b'\xAE')

    def reverse(self, x):
        if x:
            self.lcdCmd(b'\xA7')
        else:
            self.lcdCmd(b'\xA6')

    def allON(self, x):
        if x:
            self.lcdCmd(b'\xA5')
        else:
            self.lcdCmd(b'\xA4')

    def setPage(self, p):
        if p < 0:
            p = 0
        elif p > MAX_PAGE-2:
            p = MAX_PAGE-2
        self.page = p
        self.lcdCmd( bytearray([0xb0 + p]) )

    def setCol(self, c):
        if c < 0:
            c = 0
        elif c > MAX_COL:
            c = MAX_COL
        self.col = c
        self.lcdCmd( bytearray([0x10 + (c >> 4)]) )
        self.lcdCmd( bytearray([0x00 + (c & 0x0f)]) )

    def setStartLine(self, start):
        if start < 0:
            start = 0
        elif start > MAX_LINE:
            start = MAX_LINE
        self.start_line = start
        self.lcdCmd(bytearray([0x40 | start]))

    def addCol(self, x):
        self.col += x
        if self.col > MAX_COL:
            self.addPage(self.col //(MAX_COL+1))
            self.col %= (MAX_COL+1)
            self.setCol(self.col)
        elif self.col < 0:
            self.col = 0
            self.setCol(0)

    def addPage(self, x):
        self.page += x
        if self.page > MAX_PAGE:
            self.page %= (MAX_PAGE+1)

        self.setPage(self.page)
        self.clearPage()

        if self.page == (self.start_line//(MAX_PAGE+1)+(MAX_PAGE-1)) % (MAX_PAGE+1):
            self.start_line += self.scrl_line * x
            self.scroll = True
            if self.start_line > MAX_LINE:
                self.start_line %= (MAX_LINE+1)
            self.setStartLine( self.start_line )

    def putchar(self, h: int, color=1):
        if h == 0x0A:
            self.addPage(1)
            self.setCol(0)
        elif h >= 0x20 and h <= 0xdf:
            if self.col+len(font[h-0x20])+1 > MAX_COL:
                self.addPage(1)
                self.setCol(0)

            if color:
                self.lcdData( font[h-0x20] )
                self.lcdData( b'\x00' )
            else:
                for x in range(len(font[h-0x20])):
                    self.lcdData( bytearray([~font[h-0x20][x]]))
                self.lcdData( b'\xFF' )
                   
            self.addCol( len(font[h-0x20])+1 )
        else:
            raise ValueError('ChrLcd.putchar(h): value is not 0x0A,0x20to0xDF.')

    def write(self, string, color=1):
        for c in string:
            c = ord(c)
            self.putchar(c, color)                

    def text(self, string, x, y, color=1):
        if y < 0:
            y = 0
        elif y > MAX_PAGE:
            y = MAX_PAGE

        y += self.start_line//8

        if y > MAX_PAGE:
            y %= (MAX_PAGE+1)
        self.scroll = False
        self.setPage(y)
        self.setCol(x)

        for c in string:
            c = ord(c)
            self.putchar(c, color)

    def clearPage(self):
        self.setCol(0)
        for c in range(0, MAX_COL, 6):
            self.lcdData( b'\x00\x00\x00\x00\x00\x00' )
           
    def fill(self, x):
        for p in range(MAX_PAGE):
            self.setPage(p)
            self.setCol(0)
            for c in range(0, MAX_COL, 6):
                if x:
                    self.lcdData( b'\xff\xff\xff\xff\xff\xff' )
                else:
                    self.lcdData( b'\x00\x00\x00\x00\x00\x00' )
        self.setPage(0)
        self.setCol(0)
        self.scroll = False
        self.setStartLine(0)

    def clear(self):
        self.fill(0)
        
    def __init__(self, SPIn=None, cs_pin=None, rs_pin=None):
        self.pins['LCD_CS'] = Pin(cs_pin, Pin.OUT)
        self.pins['LCD_RS'] = Pin(rs_pin, Pin.OUT)

        self.pins['LCD_CS'].on()
        self.pins['LCD_RS'].on()

        self.SPI = SPIn
        self.SPI.init( baudrate=20000000, polarity=1, phase=1 )

        self.show(0)
                
        self.lcdCmd( b'\xA0\xC8\xA3' )

        self.lcdCmd(b'\x2C')                   # internal regulator
        sleep_ms(2)
        self.lcdCmd(b'\x2E')
        sleep_ms(2)
        self.lcdCmd(b'\x2F')

        self.setContrast(3, 0x1c)
        self.allON(0)
        self.reverse(0)
        self.show(1)

