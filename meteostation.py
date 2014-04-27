from meteoLib import *

configFileName = "meteo.config"   # name of the generated config file
delay = 600   # delay between uplading
username = ""   # username for uploading meteo data
password = ""   # password for uploading meteo data

m = Meteostation(configFileName)
i = 0
while True:
	data = m.getData()
	result =  m.sendData(username,password,data)
	m.log(dict(data.items() + result[1].items()))
	print "["+str(i)+"]["+time.strftime("%H:%M:%S", time.gmtime())+"] "+str(data)+" || result: "+str(result[1]["cod"])+" stationID: "+str(result[1]["id"])
	i += 1
	time.sleep(delay)
