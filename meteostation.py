from meteoLib import *

configFileName = "meteo.config"
delay = 600
username = ""
password = ""

m = Meteostation(configFileName)
i = 0
while True:
	data = m.getData()
	m.log(data)
	result =  m.sendData(username,password,data)
	print "["+str(i)+"]["+time.strftime("%H:%M:%S", time.gmtime())+"] "+str(data)+" || result: "+str(result[1]["cod"])+" stationID: "+str(result[1]["id"])
	time.sleep(delay)
	i += 1
