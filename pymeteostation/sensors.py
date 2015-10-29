from time import sleep

class Sensor:
	def __init__(self,i2c_device,settings):
		self.device = i2c_device
		self.settings = settings

	def _getData(self):
		return [0]


class sht25(Sensor):
	def _getData(self):
		self.device.route()
		return [self.device.get_hum(),self.device.get_temp()]

class altimet01(Sensor):
	def _getData(self):
		self.device.route()
		data = self.device.get_tp()
		return [data[0],data[1]/100.0]

class atmega(Sensor):
	def _getData(self):
		data = [0xFF,0xFF,0xFF]

		self.device.put(0)					# start wind speed data measurement
		sleep(1)
		data[0] = self.device.get()/2.0 	# get measured values
		
		for i in range(3):
			self.device.put(1)				# get wind direction data
			result = self.device.get()*45
			if result < 20:
				data[1] = result*45
				break

		self.device.put(2)					# get rain data
		data[2] = self.device.get()

		return data

sensor_classes = {"sht25":sht25, "altimet01": altimet01, "atmega": atmega}
