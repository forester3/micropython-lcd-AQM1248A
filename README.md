# micropython-lcd-AQM1248A
A character display class for controlling the mini graphic LCD AQM1248A with the micropython esp8266.

There are one external dependences, it is **"machine"** class.

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

