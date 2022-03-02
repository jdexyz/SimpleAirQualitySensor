import time
from adafruit_magtag.magtag import MagTag
from adafruit_magtag.graphics import Graphics
from adafruit_progressbar.progressbar import HorizontalProgressBar
import board
import alarm

import sensors


sensors.init_connected_sensors()

magtag = MagTag(rotation=0)

W = magtag.graphics.display.width
H = magtag.graphics.display.height
M = 3 # Margin

SLEEP = True


print(sensors.enabled_sensors)

def get_battery_progress():
    progress = 100*(magtag.peripherals.battery-3.6)/(4.1-3.6)
    if(progress > 100):
        progress = 100
    elif (progress < 0):
        progress = 0
    return progress


# # Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (W-30-M, H-10 - M),
    (30, 10),
    fill_color=0xFFFFFF,
    outline_color=0x000000,
    bar_color=0x777777,
)
magtag.graphics.splash.append(progress_bar)
progress_bar.progress = get_battery_progress()

texts = dict()
index = 0
current_position = 0
small_font_height = 13
big_font_height = 44

def add_text(name, text_position, text_scale, text_font, text_anchor_point):
    global index
    global texts
    texts[name] = index
    index+= 1
    magtag.add_text(
            text_position=text_position,
            text_scale=text_scale,
            text_font=text_font,
            text_anchor_point=text_anchor_point
    )

def set_text(name, text, auto_refresh=False):
    magtag.set_text(text, texts[name], auto_refresh)
    

current_position = M

if(sensors.enabled_sensors['SCD41']):
    add_text( 
            "CO2_title",
            text_position=(M,current_position,),
            text_scale=1,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(0, 0),  # top left,
    )
    set_text(name = "CO2_title", text = "CO2", auto_refresh=False)

    add_text( 
            "ppm_title",
            text_position=(W - M, current_position,),
            text_scale=1,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(1, 0),  # top right,
    )
    set_text(name = "ppm_title", text="ppm", auto_refresh=False)

    current_position += small_font_height

    add_text(
            "CO2_value",
            text_position=(W - M,current_position,),
            text_scale=3,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(1, 0),  # top right
    )

    current_position += big_font_height

    add_text(
        "Temp_value",
            text_position=(W - M, current_position,),
            text_scale=3,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(1, 0),  # top left
    )

    current_position += big_font_height

    add_text(
        "humidity_value",
            text_position=(W - M,current_position,),
            text_scale=3,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(1, 0),  # top left
    )

    current_position += big_font_height

if(sensors.enabled_sensors['CCS811']):
    add_text( 
            "VOC_title",
            text_position=(M,current_position,),
            text_scale=1,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(0, 0),  # top left,
    )
    set_text(name = "VOC_title", text="VOC", auto_refresh=False)

    add_text(  
            "ppb_title",
            text_position=(W - M, current_position,),
            text_scale=1,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(1, 0),  # top right,
    )
    set_text(name = "ppb_title", text="pbb", auto_refresh=False)

    current_position += small_font_height


    add_text( 
            "VOC_value",
            text_position=(W - M,current_position,),
            text_scale=3,
            text_font="fonts/Arial-Bold-12.pcf",
            text_anchor_point=(1, 0),  # top right
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




# magtag.set_text("%d" % scd4x.CO2, 2, auto_refresh=False)
# magtag.set_text("%0.f°C" % scd4x.temperature, 3, auto_refresh=False)
# magtag.set_text("%0.f%%" % scd4x.relative_humidity, 4, auto_refresh=False)


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

# magtag.refresh()
# while True:
#     pass


magtag.peripherals.neopixel_disable = True
magtag.peripherals.buttons[0].deinit()
a_alarm = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True) #note pull

while True:
    if(magtag.peripherals.button_b_pressed):
        SLEEP = not SLEEP
    sensors.refresh_readings()
    if(sensors.enabled_sensors['SCD41']):
        set_text(name = "CO2_value", text= "%d" % sensors.readings['CO2'], auto_refresh=False)
        set_text(name = "Temp_value", text= "%0.f°C" % sensors.readings['temperature'], auto_refresh=False)
        set_text(name = "humidity_value", text= "%0.f%%" % sensors.readings['relative_humidity'], auto_refresh=False)
    if(sensors.enabled_sensors['CCS811']):
        set_text(name = "VOC_value", text= "%d" % sensors.readings['TVOC'], auto_refresh=False)
    progress_bar.progress = get_battery_progress()
    magtag.refresh()
    if(SLEEP):
        sensors.put_sensors_to_sleep()
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 600) # 600 seconds = 5 minutes
        alarm.exit_and_deep_sleep_until_alarms(time_alarm, a_alarm)
    else:
        time.sleep(1)