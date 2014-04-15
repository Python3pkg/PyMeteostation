# MeteostationSW

Software for meteostations in Python.

## Instalation
### Dependencies

MeteostationSW needs:
* MLAB-I2c-modules (https://github.com/MLAB-project/MLAB-I2c-modules)
* requests library (http://docs.python-requests.org)

### How to

Into generateConfig.py insert required values (descripted in generateConfig.py) and run:

```
python generateConfig.py
```
## Usage
### Example

```python
from meteoLib import *

configFileName = "meteo.config"   # name of the generated config file
delay = 600   # delay between uplading
username = ""   # username for uploading meteo data
password = ""   # password for uploading meteo data

m = Meteostation(configFileName)
i = 0
while True:
	data = m.getData()
	m.log(data)
	result =  m.sendData(username,password,data)
	print "["+str(i)+"]["+time.strftime("%H:%M:%S", time.gmtime())+"] "+str(data)+" || result: "+str(result[1]["cod"])+" stationID: "+str(result[1]["id"])
	time.sleep(delay)
	i += 1


```
