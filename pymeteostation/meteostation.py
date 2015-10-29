from pymlab import config
from sensors import *
from time import time, sleep
import configobj


class Meteostation:
	def __init__(self,settings):
		self.settings = settings
		self.Devices = {}

		cfg = config.Config(i2c={"port":self.settings["I2C_Bus"]["port"]}, bus=self.settings["I2C_Bus"]["children"])
		cfg.initialize()

		for device_name, device_type in self.__getSensors(self.settings["I2C_Bus"]["children"]).items():
			if device_type in sensor_classes:
				self.Devices[device_name] = sensor_classes[device_type](cfg.get_device(device_name), self.settings)

		sleep(0.5)

	def getData(self,requestList="all"):        # returns requested sensor data
		outputList = {}
		outputList["time"] = int(time())
		
		if requestList == "all":
			requestList = self.Devices.keys()

		for device in requestList:
			outputList[device] = self.Devices[device]._getData()

		return outputList

	def __getSensors(self,bus):  # recursively searches for all "name" and "type" dictionary keys and return their values: {name:type, ...}
		names = {}
		for device in bus:
			if "name" in device and "type" in device:
				names[device["name"]] = device["type"]
			if "children" in device:
				names = dict(names.items() + self.__getSensors(device["children"]).items())
		return names

def get_I2C_configuration(i2c_bus):
	to_do = [i2c_bus]
	done = []
	while not len(to_do) == 0:
		bus = to_do[0]
		bus["children"] = []
		moved_children = []

		for item_name in bus:
			try: bus[item_name] = int(bus[item_name],base=0)
			except: pass

			if type(bus[item_name]) == configobj.Section:
				bus["children"].append(bus[item_name])
				bus["children"][len(bus["children"])-1]["name"] = item_name
				moved_children.append(item_name)
				to_do.append(bus["children"][len(bus["children"])-1])

		if len(bus["children"]) == 0:
			del bus["children"]

		for child in moved_children:
			del bus[child]

		del to_do[0]

	return i2c_bus