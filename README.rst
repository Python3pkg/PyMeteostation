==============
PyMeteostation
==============

PyMeteostation is software made for controlling meteostation built of MLAB electronic modules (http://www.mlab.cz/).

Currently supported sensors are:

* SHT25v01A (Sensirion SHT25)
* ALTIMET01A (MPL3115A2)

Software dependencies
=====================

* Pymlab (>= 0.2, https://pypi.python.org/pypi/pymlab/)

How to
======

1. Install PyMeteostation::
    
    python setup.py install

2. Install the AWS02A weewx driver:
    
    Copy the aws02a.py driver into your weewx instalation
    
    ::

        cp weewx_driver/aws02a.py /home/weewx/bin/weewx/driver/

3. Set AWS02A in weewx configuration file:

   * *[Station]* section:

      station_type = AWS02A
     
   * *[AWS02A]* section:
      
      driver = weewx.drivers.aws02a

   * *[[I2C_Bus]]* section:

      Enter I2C configuration. (example options: *type*, *address*, *channel*...)

      Section names must be unique.

   * *[[Sensor_mapping]]* section:
     
      Into option, which you want to send, fill sensor name, from which will be gathered data, and sensor measurement ID.

     See example for more information.

4. Start weewx


   **Example**::
  
      [Station]

          # Description of the station location
          location = Testovaci stanice Svakov

          # Latitude and longitude in decimal degrees
          latitude = 90.000
          longitude = 0.000

          # Altitude of the station, with unit it is in. This is downloaded from
          # from the station if the hardware supports it.
          altitude = 412, meter    # Choose 'foot' or 'meter' for unit

          # Set to type of station hardware. There must be a corresponding stanza
          # in this file with a 'driver' parameter indicating the driver to be used.
          station_type = AWS01A

          # If you have a website, you may specify an URL
          #station_url = http://www.example.com

          # The start of the rain year (1=January; 10=October, etc.). This is
          # downloaded from the station if the hardware supports it.
          rain_year_start = 1

          week_start = 6

      ##############################################################################

      [AWS01A]
          driver = weewx.drivers.aws02a

          [[I2C_Bus]]
              port = 1
              [[[barometer]]]
                  type = altimet01
                  address = 0x60
              [[[hum_temp]]]
                  type = sht25
                  address = 0x40

          [[Sensor_mapping]]
              outTemp = barometer, 0
              pressure = barometer, 1
              outHumidity = hum_temp, 0
