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
		return [data[0],data[1]/((1-((0.0065*self.settings["altitude"])/288.15))**5.255781292873008*100)]

class atmega(Sensor):
	def _getData(self):
		data = self.device.get()
		while data[0] > 20:
			data = self.device.get()
		return [data[0]*45]

sensor_classes = {"sht25":sht25, "altimet01": altimet01, "atmega": atmega}