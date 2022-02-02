# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
from adafruit_magtag.magtag import MagTag
from adafruit_magtag.graphics import Graphics
import board
# import alarm
# from adafruit_progressbar.progressbar import HorizontalProgressBar


import adafruit_scd4x
import adafruit_ccs811
# import adafruit_bme680
from adafruit_pm25.i2c import PM25_I2C
# from mics6814 import MICS6814
# import busio

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = busio.I2C(board.SCL, board.SDA)
magtag = MagTag()



button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
button_tones = (1047, 1318, 1568, 2093)

SLEEP = True
use_ccs811 = False
use_pm25 = False
# use_bme688 = False
use_MICS6814 = False
use_SCD41 = True
BIG_PPM = True


if(use_ccs811):
    ccs811 = adafruit_ccs811.CCS811(i2c)
    # Wait for the sensor to be ready
    while not ccs811.data_ready:
        pass
    # magtag.set_text("CO2: {} PPM\n TVOC: {} PPB".format(ccs811.eco2, ccs811.tvoc))

if(use_pm25):
    pm25_reset_pin = None
    pm25 = PM25_I2C(i2c, pm25_reset_pin)
    aqdata = None
    while aqdata is None:
        try:
            aqdata = pm25.read()
            # print(aqdata)
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            time.sleep(1)
    # magtag.set_text(
    #     "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
    #     % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    # )

if(use_SCD41):
    scd4x = adafruit_scd4x.SCD4X(i2c)
    scd4x.start_periodic_measurement()
    while scd4x.CO2 is None :
        time.sleep(0.1)
    # magtag.set_text("CO2: %d ppm" % scd4x.CO2)
    # magtag.set_text("Temperature: %0.1f *C" % scd4x.temperature)
    # magtag.set_text("Humidity: %0.1f %%" % scd4x.relative_humidity)

# if(use_bme688):
#     bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False, address=0x76)
#     # change this to match the location's pressure (hPa) at sea level
#     bme680.sea_level_pressure = 1013.25
#     # You will usually have to add an offset to account for the temperature of
#     # the sensor. This is usually around 5 degrees but varies by use. Use a
#     # separate temperature sensor to calibrate this one.
#     temperature_offset = -5
#     # print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
#     # print("Gas: %d ohm" % bme680.gas)
#     # print("Humidity: %0.1f %%" % bme680.relative_humidity)
#     # print("Pressure: %0.3f hPa" % bme680.pressure)
#     # print("Altitude = %0.2f meters" % bme680.altitude)

if use_MICS6814:
    mics6814 = MICS6814(i2c)
    mics6814.set_led(20,0,0)
    mics6814.set_brightness(0.1)

if(BIG_PPM):
    magtag.add_text(text_position=(3,90,),text_scale=3,
    text_font="fonts/Arial-Bold-12.pcf",
    ) #Temp
    magtag.add_text(text_position=(190,90,),text_scale=3,
    text_font="fonts/Arial-Bold-12.pcf",
    ) #Hum
    magtag.add_text(text_position=(3,30,),text_scale=4,
    text_font="fonts/Arial-Bold-12.pcf",
    ) # CO2
else:
    magtag.add_text(text_position=(3,5,),text_scale=2,) #Temp
    magtag.add_text(text_position=(3,25,),text_scale=2,) #Hum
    magtag.add_text(text_position=(3,45,),text_scale=2,) # CO2
magtag.add_text(text_position=(3,65,),text_scale=2,) #  bme688 GAS 
magtag.add_text(text_position=(3,85,),text_scale=2,) #  bme688 GAS
magtag.add_text(text_position=(3,105,),text_scale=2,) #  bme688 GAS

magtag.add_text(text_position=(250,10,),text_scale=2,) #  Battery



# # Create a new progress_bar object at (x, y)
# progress_bar = HorizontalProgressBar(
#     (200, 20),
#     (30, 10),
#     bar_color=0xFFFFFF,
#     outline_color=0xAAAAAA,
#     fill_color=0x777777,
# )



# set up pin alarms
# pin_alarms = [alarm.pin.PinAlarm(pin=board.BUTTON_, value=False, pull=True)]

magtag.peripherals.neopixel_disable = True


while True:
    # for i, b in enumerate(magtag.peripherals.buttons):
    #     if not b.value:
    #         print("Button %c pressed" % chr((ord("A") + i)))
    #         magtag.peripherals.neopixel_disable = False
    #         magtag.peripherals.neopixels.fill(button_colors[i])
    #         magtag.peripherals.play_tone(button_tones[i], 0.25)
    #         break
    # else:
    #   magtag.peripherals.neopixel_disable = True
    if(use_SCD41):
        if(BIG_PPM):
            magtag.set_text("%0.f°C" % scd4x.temperature, 0, auto_refresh=False)
            magtag.set_text("%0.f%%" % scd4x.relative_humidity, 1, auto_refresh=False)
            magtag.set_text("%dppm" % scd4x.CO2, 2, auto_refresh=False)
        else:
            magtag.set_text("T %0.1f*C" % scd4x.temperature, 0, auto_refresh=False)
            magtag.set_text("H %0.1f%%" % scd4x.relative_humidity, 1, auto_refresh=False)
            magtag.set_text("CO2 %dppm" % scd4x.CO2, 2, auto_refresh=False)
    # if(use_bme688):
    #     # magtag.set_text("T %0.1f*C" % float(bme680.temperature) + temperature_offset, 0, auto_refresh=False)
    #     magtag.set_text("GAS %dohm" % bme680.gas, 2, auto_refresh=False)
    #     # print("\nTemperature: %0.1f C" % ())
    if(use_pm25):
        try:
            aqdata = pm25.read()
            magtag.set_text(
                "PM1.0 %d" % (aqdata["pm10 standard"]),
                 2, auto_refresh=False)
            magtag.set_text(
                "PM2.5 %d" % (aqdata["pm25 standard"]),
                 3, auto_refresh=False)
            magtag.set_text(
                "PM10 %d" % (aqdata["pm100 standard"]),
                 4, auto_refresh=False)
        except RuntimeError:
            print("Unable to read from sensor, retrying...")

    voltage = magtag.peripherals.battery
    magtag.set_text("%f" % voltage, 6, auto_refresh=False)
    magtag.refresh()
    if(SLEEP):
        if(use_SCD41):
            scd4x.stop_periodic_measurement()
        # alarm.exit_and_deep_sleep_until_alarms(*pin_alarms)
        magtag.exit_and_deep_sleep(10*60)  # 5 minutes
    time.sleep(5)