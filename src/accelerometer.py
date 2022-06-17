import adafruit_lis3dh

# get the display
epd = board.DISPLAY

# set up accelerometer
lis = adafruit_lis3dh.LIS3DH_I2C(board.I2C(), address=0x19)

# See: ST Design Tip DT0008 - Simple screen rotation using
#      the accelerometer built-in 4D detection interrupt
# pylint: disable=protected-access
lis._write_register_byte(0x20, 0x3F)  # low power mode with ODR = 25Hz
lis._write_register_byte(0x22, 0x40)  # AOI1 interrupt generation is routed to INT1 pin
lis._write_register_byte(0x23, 0x80)  # FS = ±2g low power mode with BDU bit enabled
lis._write_register_byte(
    0x24, 0x0C
)  # Interrupt signal on INT1 pin is latched with D4D_INT1 bit enabled
lis._write_register_byte(
    0x32, 0x20
)  # Threshold = 32LSBs * 15.625mg/LSB = 500mg. (~30 deg of tilt)
lis._write_register_byte(0x33, 0x01)  # Duration = 1LSBs * (1/25Hz) = 0.04s
