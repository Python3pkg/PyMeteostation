from pymlab import config
from sensors import *
from time import time, sleep


class Meteostation:
	def __init__(self,settings):
		self.settings = settings
		self.Devices = {}

		try:
			cfg = config.Config(i2c={"port":self.settings["I2C_configuration"]["port"]}, bus=self.settings["I2C_configuration"]["bus"])
			cfg.initialize()

			sensors = self.__getSensors(self.settings["I2C_configuration"]["bus"])
			for device in sensors.keys():
				self.Devices[device] = sensor_classes[sensors[device]](cfg.get_device(device), self.settings)

		except Exception, e:
			raise Exception("Initialization of I2c failed: "+str(e))

		sleep(0.5)

	def getData(self,requestList="all"):        # returns requested sensor data
		outputList = {}
		outputList["time"] = int(time())
		
		if requestList == "all":
			devices = self.Devices.keys()
		else:
			devices = requestList
		for device in devices:
			outputList[device] = self.Devices[device]._getData()

		return outputList

	def __getSensors(self,busConfig):  # recursively searches for all "name" and "type" dictionary keys and return their values: {name:type, ...}
		names = {}
		for item in busConfig:
			for key in item.keys():
				if key == "name":
					names[item[key]] = item["type"]
				if type(item[key]) == list:
					names = dict(names.items() + self.__getSensors(item[key]).items())
		return names