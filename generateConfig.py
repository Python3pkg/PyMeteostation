import json

configBus = [					# configuration of I2c bus, supported sensor names: barometer, hum_temp
            	{"type": "i2chub",
             	 "address": 0x72,
             	 "children": 
             	 	[
                    	{"type": "i2chub","address": 0x70,"channel": 0,"children": 
                    		[
                				{"name": "barometer", "type": "altimet01" , "channel": 0},
                				{"name": "hum_temp", "type": "sht25" , "channel": 1}
                    		]
                    	}
                	]
            	}
        	]

deviceNameList = ["barometer","hum_temp"]    # list of sensor names

translationConfig = [["wind_dir","",""],["wind_speed","",""],["wind_gust","",""],["temp","hum_temp","1"],["humidity","hum_temp","0"],
                    ["pressure","barometer","1"],["rain_1h","",""],["rain_24h","",""],["rain_today","",""],["snow","",""],
                    ["lum","",""],["radiation","",""],["dew_point","",""],["uv","",""]]	# assignment of sensor values to openweathermap.com value names
                    					# example: [OWM.com name, sensor name, sensor value ID (only if sensor returns more than 1 value)]

logFileName = "log.txt"		# name of log file

stationName = ""      # string or False
latitude = 0.0        # float or False
longitude = 0.0       # float or False
altitude = 0.0        # float or False, must be filled if you use altimet01 sensor

with open("meteo.config","w") as f:
	f.write(json.dumps({"configBus":configBus,"deviceNameList":deviceNameList,"translationConfig":translationConfig,"logFileName":logFileName,"stationName":stationName,"latitude":latitude,"longitude":longitude,"altitude":altitude}))
