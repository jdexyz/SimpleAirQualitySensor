# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
from adafruit_magtag.magtag import MagTag
import adafruit_scd4x
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

reset_pin = None


magtag = MagTag()

magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=2,
)

magtag.set_text("PGT POWER")

button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
button_tones = (1047, 1318, 1568, 2093)

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
pm25 = PM25_I2C(i2c, reset_pin)
# i2c = board.I2C()
# scd4x = adafruit_scd4x.SCD4X(i2c)
# print("Serial number:", [hex(i) for i in scd4x.serial_number])

# scd4x.start_periodic_measurement()
print("Waiting for first measurement....")


while True:
    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            print("Button %c pressed" % chr((ord("A") + i)))
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(button_colors[i])
            magtag.peripherals.play_tone(button_tones[i], 0.25)
            break
    else:
        magtag.peripherals.neopixel_disable = True
    
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    magtag.set_text(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    # if scd4x.data_ready:
        # magtag.set_text("CO2: %d ppm" % scd4x.CO2)
        # magtag.set_text("Temperature: %0.1f *C" % scd4x.temperature)
        # magtag.set_text("Humidity: %0.1f %%" % scd4x.relative_humidity)
        # magtag.set_text("PGT POWER")
        # print()
    time.sleep(1)