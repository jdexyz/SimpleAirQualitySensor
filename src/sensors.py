import board
import alarm
import time

import busio

i2c = busio.I2C(board.SCL, board.SDA)

import PCA9536

i2cSwitch = PCA9536.PCA9536(i2c)

pm25 = None
scd4x = None
mics6814 = None
ccs811 = None

CCS811_LOW_POWER_MODE = None

i2cSwitch.powerOff()

# print(i2cSwitch.read(0))

def init_sensor(sensor):
	global pm25
	global scd4x
	global mics6814
	global ccs811
	global CCS811_LOW_POWER_MODE
	if(sensor == 'PM25'):
		from adafruit_pm25.i2c import PM25_I2C
		pm25_reset_pin = None
		pm25 = PM25_I2C(i2c, pm25_reset_pin)
		aqdata = pm25.read()
		while aqdata is None:
			try:
				pm25.read()
			except RuntimeError:
				time.sleep(0.1)
	elif(sensor == 'SCD41'):
		import adafruit_scd4x
		scd4x = adafruit_scd4x.SCD4X(i2c)
		scd4x.start_periodic_measurement()
		while scd4x.CO2 is None :
			time.sleep(0.1)
	elif(sensor == 'MICS6814'):
		from mics6814 import MICS6814 
		mics6814 = MICS6814(i2c)
		# mics6814.set_led(0,0,0)
		# mics6814.set_brightness(0)
	elif(sensor == 'CCS811'):
		import adafruit_ccs811
		ccs811 = adafruit_ccs811.CCS811(i2c)
		CCS811_LOW_POWER_MODE = adafruit_ccs811.DRIVE_MODE_60SEC
		# Wait for the sensor to be ready
		while not ccs811.data_ready:
			time.sleep(0.1)

readings = dict()

def refresh_readings():
	global pm25
	global scd4x
	global mics6814
	global ccs811
	#i2cSwitch.powerOn()
	# if(enabled_sensors['PM25']):
		# init_sensor('PM25')
	if(enabled_sensors['SCD41']):
		readings['CO2'] = scd4x.CO2
		readings['temperature'] = scd4x.temperature
		readings['relative_humidity'] = scd4x.relative_humidity
	# if enabled_sensors['MICS6814']:
	if enabled_sensors['CCS811']:
		readings['TVOC'] = ccs811.tvoc
		readings['eCO2'] = ccs811.eco2
	return readings


def put_sensors_to_sleep():
	global pm25
	global scd4x
	global mics6814
	global ccs811
	if(enabled_sensors['SCD41']):
		scd4x.stop_periodic_measurement()
	if(enabled_sensors['CCS811']):
		ccs811.drive_mode = CCS811_LOW_POWER_MODE
	i2cSwitch.powerOff()

while not i2c.try_lock():
	time.sleep(0.1)

addresses = i2c.scan()
i2c.unlock()

print("Detected i2C addresses", addresses)

enabled_sensors = dict(
	PM25 = 0x12 in addresses,
	SCD41 = 0x62 in addresses,
	MICS6814 = 0x19 in addresses and False,
	CCS811 = 0x5a in addresses,
)

def init_connected_sensors():
	if(enabled_sensors['PM25']):
		init_sensor('PM25')
	if(enabled_sensors['SCD41']):
		init_sensor('SCD41')
	if enabled_sensors['MICS6814']:
		init_sensor('MICS6814')
	if enabled_sensors['CCS811']:
		init_sensor('CCS811')