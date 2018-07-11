# micropython-lcd-AQM1248A
A character display class for controlling the mini graphic LCD AQM1248A with the micropython esp8266.

There are one external dependences, it is **"machine"** class.

## New module aqm1248largechrlcd  

Displayed large font size is 15x21.
### Usage
~~~
import machine
import aqm1248largechrlcd
hspi = machine.SPI(1)
lcd = aqm1248largechrlcd.LargeChrLcd( hspi, cs_pin=2, rs_pin=15 )
lcd.clear()
lcd.write( 'Micro\n' )
lcd.write( 'Python' )  
~~~
## Second module aqm1248midchrlcd

Displayed medium font size is 10x14.  
### Usage
~~~
import machine
import aqm1248midchrlcd
hspi = machine.SPI(1)
lcd = aqm1248midchrlcd.MidChrLcd( hspi, cs_pin=2, rs_pin=15 )
lcd.clear()
lcd.write( 'Hello, AQM1248A !' )
lcd.text('Micro', 12, 2)  
~~~
In text() method, the page number is only even number.  
(column = 12, page =2) means to display a medium size font on the 2nd column of the 2nd line.

## First module aqm1248chrlcd
### Usage

use hardware SPI
~~~
import machine
hspi = machine.SPI(1)
import aqm1248chrlcd
lcd = aqm1248chrlcd.ChrLcd( hspi, cs_pin=2, rs_pin=15 )
lcd.clear()
lcd.write( 'Hello, AQM1248A !' )
~~~
use software SPI
~~~
import machine
sspi = machine.SPI(-1, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12) )
import aqm1248chrlcd
lcd = aqm1248chrlcd.ChrLcd( sspi, cs_pin=2, rs_pin=15 )
lcd.clear()
lcd.text( 'Hello, World !!', 3, 3 )
~~~
### usage of text() method  
The second argument is column, the range is from 0 to 128.  
The third argument is page, the range is form 0 to 5.
