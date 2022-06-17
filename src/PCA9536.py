import time
PCA9536_I2C_ADDR = 0x41  #default i2c adress

# // PCA9536 registers:
# typedef enum {
PCA9536_REGISTER_INPUT_PORT         = 0x00
PCA9536_REGISTER_OUTPUT_PORT        = 0x01
PCA9536_REGISTER_POLARITY_INVERSION = 0x02
PCA9536_REGISTER_CONFIGURATION      = 0x03
# } PCA9536_REGISTER_t;

# // PCA9536 error code returns:
# typedef enum {
PCA9536_ERROR_READ            = -4
PCA9536_ERROR_WRITE           = -3
PCA9536_ERROR_INVALID_ADDRESS = -2
PCA9536_ERROR_UNDEFINED       = -1
PCA9536_ERROR_SUCCESS         = 1
# } PCA9536_error_t;
# const PCA9536_error_t PCA9536_SUCCESS = PCA9536_ERROR_SUCCESS;

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 0

class PCA9536():
    def __init__(self, i2c, i2c_addr=PCA9536_I2C_ADDR):
        self._i2c = i2c
        self._i2c_addr = i2c_addr


    def i2c_read8(self, reg):
        buf = bytearray([0])
        while (not self._i2c.try_lock()):
            time.sleep(0.01)
        self._i2c.writeto_then_readfrom(self._i2c_addr, bytearray([reg]), buf)
        self._i2c.unlock()
        return buf[0]

    def i2c_write8(self, reg, value):
        while (not self._i2c.try_lock()):
            time.sleep(0.01)
        msg_w = self._i2c.writeto(self._i2c_addr,bytearray([reg, value]))
        self._i2c.unlock()

    def setPinMode(self, pin, mode):
        configRegister = self.i2c_read8(PCA9536_REGISTER_CONFIGURATION)
        configRegister &= ~(1<<pin) # Clear pin bit        
        if (mode == INPUT): # Set the bit if it's being set to INPUT (opposite of Arduino)
            configRegister |= (1<<pin);
        self.i2c_write8(PCA9536_REGISTER_CONFIGURATION, configRegister)

    def write(self, pin, value):
        outputRegister = self.i2c_read8(PCA9536_REGISTER_OUTPUT_PORT)
        outputRegister &= ~(1<<pin)
        if (value == HIGH): # Set the bit if it's being set to HIGH (opposite of Arduino)
            outputRegister |= (1<<pin)
        self.i2c_write8(PCA9536_REGISTER_OUTPUT_PORT, outputRegister)

    def read(self, pin):
        inputRegister = self.i2c_read8(PCA9536_REGISTER_INPUT_PORT)
        return (inputRegister & (1<<pin)) >> pin

    def powerOn(self):
          self.setPinMode(0, OUTPUT) # Make GPIO0 an output
          self.write(0, HIGH) # Set the output

    def powerOff(self):
        self.i2c_write8(PCA9536_REGISTER_CONFIGURATION, 0b00000000)
        self.i2c_write8(PCA9536_REGISTER_OUTPUT_PORT, 0x00)


    ## Strangely do not work...
    
    # def powerOff(self): 
    #       self.setPinMode(0, INPUT) # Make GPIO0 an output
    #       self.write(0, LOW) # Set the output

    #       # self.setPinMode(3, OUTPUT) # Make GPIO3 an output
    #       # self.write(3, HIGH) # Set the output

    # def isolationOn(self):
    #     self.setPinMode(3, OUTPUT) # Make GPIO0 an output
    #     self.write(3, LOW) # Set the output

    # def isolationOff(self):
    #     self.setPinMode(3, OUTPUT) # Make GPIO0 an output
    #     self.write(3, HIGH) # Set the output



# PCA9536_error_t QWIIC_POWER::isolationOn()
# {
#   // Enable I2C isolation = I2C bus _is_ isolated
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, LOW); // Set the output low

#   return PCA9536_ERROR_SUCCESS;
# }

# PCA9536_error_t QWIIC_POWER::isolationOff()
# {
#   // Disable I2C isolation = I2C bus _is not_ isolated
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, HIGH); // Set the output high

#   return PCA9536_ERROR_SUCCESS;
# }

# boolean QWIIC_POWER::begin(TwoWire &wirePort)
# {
#   _i2cPort = &wirePort; //Grab which port the user wants us to use
#   _deviceAddress = PCA9536_ADDRESS;

#   //Check connection
#   if (isConnected() == false)
#     return (false);

#   // Enable Qwiic Power
#   pinMode(0, OUTPUT); // Make GPIO0 an output
#   write(0, HIGH); // Set the output high

#   // Enable I2C
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, HIGH); // Set the output high

#   return (true);
# }

# //Returns true if I2C device ack's
# boolean QWIIC_POWER::isConnected()
# {
#   _i2cPort->beginTransmission((uint8_t)_deviceAddress);
#   return ((_i2cPort->endTransmission()) == 0);
# }

# PCA9536_error_t QWIIC_POWER::powerOn()
# {
#   // Enable Qwiic Power
#   pinMode(0, OUTPUT); // Make GPIO0 an output
#   write(0, HIGH); // Set the output high

#   // Enable I2C
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, HIGH); // Set the output high

#   return PCA9536_ERROR_SUCCESS;
# }

# PCA9536_error_t QWIIC_POWER::powerOff()
# {
#   // Disable Qwiic Power
#   pinMode(0, OUTPUT); // Make GPIO0 an output
#   write(0, LOW); // Set the output low

#   // Disable I2C
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, LOW); // Set the output low

#   return PCA9536_ERROR_SUCCESS;
# }

# PCA9536_error_t QWIIC_POWER::switchPower(uint8_t value)
# {
#   pinMode(0, OUTPUT); // Make GPIO0 an output
#   write(0, value); // Set the output

#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, value); // Set the output

#   return PCA9536_ERROR_SUCCESS;
# }

# PCA9536_error_t QWIIC_POWER::isolationOn()
# {
#   // Enable I2C isolation = I2C bus _is_ isolated
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, LOW); // Set the output low

#   return PCA9536_ERROR_SUCCESS;
# }

# PCA9536_error_t QWIIC_POWER::isolationOff()
# {
#   // Disable I2C isolation = I2C bus _is not_ isolated
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   write(3, HIGH); // Set the output high

#   return PCA9536_ERROR_SUCCESS;
# }

# PCA9536_error_t QWIIC_POWER::switchIsolation(uint8_t value)
# {
#   pinMode(3, OUTPUT); // Make GPIO3 an output
#   if (value == 0) // If value is 0
#   {
#     write(3, HIGH); // Set the output high to disable isolation
#   }
#   else
#   {
#     write(3, LOW); // Set the output low to enable isolation
#   }

#   return PCA9536_ERROR_SUCCESS;
# }




# # uint8_t QWIIC_POWER::read(uint8_t pin)
# # {
# #   PCA9536_error_t err;
# #   uint8_t inputRegister = 0;

# #   if (pin > 4) return PCA9536_ERROR_UNDEFINED;

# #   err = readI2CRegister(&inputRegister, PCA9536_REGISTER_INPUT_PORT);
# #   if (err != PCA9536_ERROR_SUCCESS)
# #   {
# #     return err;
# #   }
# #   return (inputRegister & (1<<pin)) >> pin;
# # }


# # PCA9536_error_t QWIIC_POWER::write(uint8_t pin, uint8_t value)
# # {
# #   PCA9536_error_t err;
# #   uint8_t outputRegister = 0;

# #   if (pin > 4) return PCA9536_ERROR_UNDEFINED;

# #   err = readI2CRegister(&outputRegister, PCA9536_REGISTER_OUTPUT_PORT);
# #   if (err != PCA9536_ERROR_SUCCESS)
# #   {
# #     return err;
# #   }
# #   // TODO: Break out of here if it's already set correctly
# #   outputRegister &= ~(1<<pin); // Clear pin bit
# #   if (value == HIGH) // Set the bit if it's being set to HIGH (opposite of Arduino)
# #   {
# #     outputRegister |= (1<<pin);
# #   }
# #   return writeI2CRegister(outputRegister, PCA9536_REGISTER_OUTPUT_PORT);
# # }
