# -*- coding: utf-8 -*-
import json
writeDict = {}
writeDict["busConfig"] = [					# configuration of I2c bus, supported sensor types: altimet01, sht25
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

writeDict["translationConfig"] = [["wind_dir","",0],   # assignment of sensor values to openweathermap.com value names
                                  ["wind_speed","",0], # example: [OWM.com name, sensor name, sensor value ID]
                                  ["wind_gust","",0],
                                  ["temp","hum_temp",1],
                                  ["humidity","hum_temp",0],
                                  ["pressure","barometer",1],
                                  ["rain_1h","",0],
                                  ["rain_24h","",0],
                                  ["rain_today","",0],
                                  ["snow","",0],
                                  ["lum","",0],
                                  ["radiation","",0],
                                  ["dew_point","",0],
                                  ["uv","",0]]	

writeDict["logPath"] = "logs/"		# path to directory where to save logs, string, fill or leave blank

writeDict["stationName"] = ""      # string or False
writeDict["latitude"] = 0.0      # float or False
writeDict["longitude"] = 0.0       # float or False
writeDict["altitude"] = 0.0        # float or False, must be filled if you use altimet01 sensor

with open("meteo.config","w") as f:
	f.write(json.dumps(writeDict))
