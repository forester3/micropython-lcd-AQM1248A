# micropython-lcd-AQM1248A
A character display class for controlling the mini graphic LCD AQM1248A with the micropython esp8266.

There are one external dependences, it is **"machine"** class.
## New module aqm1248_midchrlcd

Displayed medium font size is 10x14.  


### Usage

    import machine
    import aqm1248_midchrlcd
    hspi = machine.SPI(1)
    lcd = aqm1248_midchrlcd.MidChrLcd( hspi, cs_pin=2, rs_pin=15 )
    lcd.clear()
    lcd.write( 'Hello, AQM1248A !' )
    lcd.text('Micro', 12, 2)  

In test() method, the page number is only even number.  
(column = 12, page =2) means to display a medium size font on the 2nd column of the 2nd line.

## Usage

use hardware SPI
~~~
import machine
hspi = machine.SPI(1)
import AQM1248_ChrLcd
lcd = AQM1248_ChrLcd.ChrLcd( hspi, cs_pin=2, rs_pin=15 )
lcd.clear()
lcd.write( 'Hello, AQM1248A !' )
~~~
use software SPI
~~~
import machine
sspi = machine.SPI(-1, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12) )
import AQM1248_ChrLcd
lcd = AQM1248_ChrLcd.ChrLcd( sspi, cs_pin=2, rs_pin=15 )
lcd.clear()
lcd.text( 'Hello, World !!', 3, 3 )
~~~
### usage of test() method  
    The second argument is column, the range is from 0 to 128.  
    The third argument is page, the range is form 0 to 5.
