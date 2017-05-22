"""AWS02A driver for the weewx weather system"""

import time,logging

import weewx.drivers
import weeutil.weeutil
import pymeteostation

DRIVER_NAME = 'AWS02A'
DRIVER_VERSION = "0.1"

def loader(config_dict, engine):
	station = AWS02A(**config_dict)
	return station
		
class AWS02A(weewx.drivers.AbstractDevice):
	def __init__(self, **stn_dict):
		self.stn_dict = stn_dict
		stn_dict[DRIVER_NAME]["I2C_Bus"] = pymeteostation.get_I2C_configuration(stn_dict[DRIVER_NAME]["I2C_Bus"])
		self.m = pymeteostation.Meteostation(stn_dict[DRIVER_NAME])

	def genLoopPackets(self):
		while True:
			data = self.m.getData()
			
			_packet = {"dateTime": data["time"],
					   "usUnits" : weewx.METRICWX}

			for packet_name in self.stn_dict[DRIVER_NAME]["Sensor_mapping"]:
				_packet[packet_name] = data[ self.stn_dict[DRIVER_NAME]["Sensor_mapping"][packet_name][0]] [int(self.stn_dict[DRIVER_NAME]["Sensor_mapping"][packet_name][1])]

			yield _packet
	
	@property
	def hardware_name(self):
		return "AWS02A"


def confeditor_loader():
	return AWS02AConfEditor()

class AWS02AConfEditor(weewx.drivers.AbstractConfEditor):
	@property
	def default_stanza(self):
		return """
[AWS02A]
	# This section is for the AWS02A weather station

	# The driver to use:
	driver = weewx.drivers.aws02a

	# I2C bus configuration:
	[[I2C_Bus]]
		port = 1

	# Sensor mapping to the weewx data
	[[Sensor_mapping]]
		#outTemp = barometer, 1

"""


if __name__ == "__main__":
	station = AWS02A(loop_interval=2.0)
	for packet in station.genLoopPackets():
		print(weeutil.weeutil.timestamp_to_string(packet['dateTime']), packet)