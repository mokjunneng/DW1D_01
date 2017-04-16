import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
try:
    while True:
        resp = spi.xfer2([0xAA])
        print spi.readbytes(8)
        time.sleep(0.1)
except KeyboardInterrupt:
    spi.close()

spi.xfer([value_8bit])