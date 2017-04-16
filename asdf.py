import spidev
import time


spi = spidev.SpiDev() # create spi object
spi.open(0, 0)
spi.max_speed_hz = 1000000
try:
    while True:
        resp = spi.xfer2([0xAA]) # transfer one byte
        print spi.readbytes(8)
        time.sleep(0.1) # sleep for 0.1 seconds
        #end while
except KeyboardInterrupt: # Ctrl+C pressed, so…
 spi.close() # … close the port before exit
#end try


spi.xfer([value_8bit])