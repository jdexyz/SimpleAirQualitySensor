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

enabled_sensors = dict(
		PM25 = False,
		SCD41 = False,
		MICS6814 = False,
		CCS811 = False,
	)
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
				aqdata = pm25.read()
			except RuntimeError:
				print('loading')
				time.sleep(0.1)
		# print('aqdata', aqdata)
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
	if enabled_sensors['PM25']:
		try:
			aqdata = pm25.read()
			readings['pm10 env'] = aqdata['pm10 env']
			readings['pm25 env'] = aqdata['pm25 env']
			readings['pm100 env'] = aqdata['pm100 env']
			readings['pm10 standard'] = aqdata['pm10 standard']
			readings['pm25 standard'] = aqdata['pm25 standard']
			readings['pm100 standard'] = aqdata['pm100 standard']
			readings['particles 03um'] = aqdata['particles 03um']
			readings['particles 05um'] = aqdata['particles 05um']
			readings['particles 10um'] = aqdata['particles 10um']
			readings['particles 25um'] = aqdata['particles 25um']
			readings['particles 50um'] = aqdata['particles 50um']
			readings['particles 100um'] = aqdata['particles 100um']
		except RuntimeError:
			readings['pm10 env'] = -1
			readings['pm25 env'] = -1
			readings['pm100 env'] = -1
			readings['pm10 standard'] = -1
			readings['pm25 standard'] = -1
			readings['pm100 standard'] = -1
			readings['particles 03um'] = -1
			readings['particles 05um'] = -1
			readings['particles 10um'] = -1
			readings['particles 25um'] = -1
			readings['particles 50um'] = -1
			readings['particles 100um'] = -1

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


def get_connected_sensors():
	global enabled_sensors
	while not i2c.try_lock():
		time.sleep(0.1)

	addresses = i2c.scan()
	i2c.unlock()

	print("Detected i2C addresses", [hex(a) for a in addresses])

	print('''

	# 	PM25 = 0x12 = 18
	# 	SCD41 = 0x62 = 98
	# 	MICS6814 = 0x19 = 25
	# 	CCS811 = 0x5a = 90
	#  	Switch = 0x41 = 65
	#	Accelero = 0x19 = 25
		''')

	# enabled_sensors = dict(
	# 	PM25 = False,
	# 	SCD41 = True,
	# 	MICS6814 = False,
	# 	CCS811 = False,
	# )
	enabled_sensors = dict(
		PM25 = 0x12 in addresses,
		SCD41 = 0x62 in addresses,
		MICS6814 = False,#0x19 in addresses and 0x12 in addresses,
		CCS811 = 0x5a in addresses,
	)
	print(enabled_sensors)


def init_connected_sensors():
	i2cSwitch.powerOff()
	time.sleep(0.1)
	i2cSwitch.powerOn()
	time.sleep(3)
	get_connected_sensors()


	if(enabled_sensors['PM25']):
		init_sensor('PM25')
	if(enabled_sensors['SCD41']):
		init_sensor('SCD41')
	if enabled_sensors['MICS6814']:
		init_sensor('MICS6814')
	if enabled_sensors['CCS811']:
		init_sensor('CCS811')