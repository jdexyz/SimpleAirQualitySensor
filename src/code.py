# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
from adafruit_magtag.magtag import MagTag
from adafruit_magtag.graphics import Graphics
from adafruit_progressbar.progressbar import HorizontalProgressBar
import board
import alarm


import adafruit_scd4x
import adafruit_ccs811
from adafruit_pm25.i2c import PM25_I2C
from mics6814 import MICS6814 
import busio

i2c = busio.I2C(board.SCL, board.SDA)

magtag = MagTag(rotation=0)

W = magtag.graphics.display.width
H = magtag.graphics.display.height
M = 3 # Margin

SLEEP = False
use_pm25 = True
use_MICS6814 = True
use_SCD41 = True
BIG_PPM = True


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

if(use_SCD41):
    scd4x = adafruit_scd4x.SCD4X(i2c)
    scd4x.start_periodic_measurement()
    while scd4x.CO2 is None :
        time.sleep(0.1)

if use_MICS6814:
    mics6814 = MICS6814(i2c)
    mics6814.set_led(0,0,0)
    mics6814.set_brightness(0)



# # Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (W-30-M, H-10 - M),
    (30, 10),
    fill_color=0xFFFFFF,
    outline_color=0x000000,
    bar_color=0x777777,
)
magtag.graphics.splash.append(progress_bar)
progress_bar.progress = 100*(magtag.peripherals.battery-3.6)/(4.1-3.6)

magtag.add_text( ## "CO2"
        text_position=(M,M,),
        text_scale=1,
        text_font="fonts/Arial-Bold-12.pcf",
        text_anchor_point=(0, 0),  # top left,
)
magtag.set_text("CO2", 0, auto_refresh=False)

magtag.add_text( ## "ppm"
        text_position=(W - M, M,),
        text_scale=1,
        text_font="fonts/Arial-Bold-12.pcf",
        text_anchor_point=(1, 0),  # top right,
)
magtag.set_text("ppm", 1, auto_refresh=False)

magtag.add_text( ## CO2 value
        text_position=(W - M,16,),
        text_scale=3,
        text_font="fonts/Arial-Bold-12.pcf",
        text_anchor_point=(1, 0),  # top right
)

magtag.add_text( ## Temp
        text_position=(W - M,60,),
        text_scale=3,
        text_font="fonts/Arial-Bold-12.pcf",
        text_anchor_point=(1, 0),  # top left
)
magtag.add_text( ## humidity
        text_position=(W - M,105,),
        text_scale=3,
        text_font="fonts/Arial-Bold-12.pcf",
        text_anchor_point=(1, 0),  # top left
)



# magtag.add_text( ## "PM1.0"
#         text_position=(5,140,),
#         text_scale=1,
#         text_font="fonts/Arial-Bold-12.pcf",
#         text_anchor_point=(0, 0),  # top left,
# )
# magtag.set_text("PM1.0", 5, auto_refresh=False)

# magtag.add_text( ## "ppm"
#         text_position=(125,140,),
#         text_scale=1,
#         text_font="fonts/Arial-Bold-12.pcf",
#         text_anchor_point=(1, 0),  # top right,
# )
# magtag.set_text("ppm", 6, auto_refresh=False)

# magtag.add_text( ## PM1.0 value
#         text_position=(125,155,),
#         text_scale=2,
#         text_font="fonts/Arial-Bold-12.pcf",
#         text_anchor_point=(1, 0),  # top right
# )




magtag.set_text("%d" % scd4x.CO2, 2, auto_refresh=False)
magtag.set_text("%0.f°C" % scd4x.temperature, 3, auto_refresh=False)
magtag.set_text("%0.f%%" % scd4x.relative_humidity, 4, auto_refresh=False)


# aqdata = pm25.read()
# magtag.set_text(
#     "%d" % (aqdata["pm10 standard"]),
#      7, auto_refresh=False)
# magtag.set_text(
#     "%d" % (aqdata["pm25 standard"]),
#      3, auto_refresh=False)
# magtag.set_text(
#     "%d" % (aqdata["pm100 standard"]),
#      4, auto_refresh=False)

# magtag.add_text(text_position=(225,10,),text_scale=2,) #  Battery

magtag.refresh()
while True:
    pass


# magtag.peripherals.neopixel_disable = True
# magtag.peripherals.buttons[0].deinit()
# a_alarm = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True) #note pull

# while True:
#     if(magtag.peripherals.button_b_pressed):
#         SLEEP = not SLEEP
#     if(use_SCD41):
#         if(BIG_PPM):
#             magtag.set_text("%0.f°C" % scd4x.temperature, 0, auto_refresh=False)
#             magtag.set_text("%0.f%%" % scd4x.relative_humidity, 1, auto_refresh=False)
#             magtag.set_text("%dppm" % scd4x.CO2, 2, auto_refresh=False)
#     if(use_pm25):
#         try:
#             aqdata = pm25.read()
#             magtag.set_text(
#                 "PM1.0 %d" % (aqdata["pm10 standard"]),
#                  2, auto_refresh=False)
#             magtag.set_text(
#                 "PM2.5 %d" % (aqdata["pm25 standard"]),
#                  3, auto_refresh=False)
#             magtag.set_text(
#                 "PM10 %d" % (aqdata["pm100 standard"]),
#                  4, auto_refresh=False)
#         except RuntimeError:
#             print("Unable to read from sensor, retrying...")

#     voltage = magtag.peripherals.battery
#     if(SLEEP):
#         magtag.set_text("S %f" % voltage, 6, auto_refresh=False)
#     else:
#         magtag.set_text("W %f" % voltage, 6, auto_refresh=False)
#     magtag.refresh()
#     if(SLEEP):
#         if(use_SCD41):
#             scd4x.stop_periodic_measurement()
#         # alarm.exit_and_deep_sleep_until_alarms(*pin_alarms)
#         time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 600) # 600 seconds = 5 minutes
#         alarm.exit_and_deep_sleep_until_alarms(time_alarm, a_alarm)
#         # magtag.exit_and_deep_sleep(10*60)  # 5 minutes
#     else:
#         # time.sleep(1)
#         time.sleep(5)