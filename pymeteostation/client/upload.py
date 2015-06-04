import urllib2, urllib, base64, json

def uploadToOWM(data,settings):      # sends data to openweathermap.com
	url = "http://openweathermap.org/data/post"
	POST = translateToPOST(data,settings)
	request = urllib2.Request(url,data=urllib.urlencode(POST),headers={"Authorization":"Basic "+base64.encodestring(settings["username"]+":"+settings["password"])[:-1]})
	try:
		result = urllib2.urlopen(request)
	except urllib2.URLError as e:
		if hasattr(e, "code"):
			return (False, {"message":e.reason,"cod":e.code,"id":"0"})
		else:
			return (False, {"message":e.reason,"cod":"Failed to reach server","id":"0"})
	except Exception as e:
		return (False, {"message":str(e),"cod":"Network error","id":"0"})
	else:
		try:
			result = result.read()
			return (True, json.loads(result))
		except Exception as e:
			return (False, {"message":result,"cod":str(e),"id":"0"})

def translateToPOST(sendDict,settings):    # translates sensor values to POST request format
	payload = {}
	for itemKey in sendDict.keys():
		if not itemKey == "time" and not sendDict[itemKey][0] == "error":
			for transList in settings["Translation_Into_POST"]:
				if itemKey == transList[1]:
					payload[transList[0]] = str(round(sendDict[itemKey][transList[2]],2))

	if settings["stationname"]:
		payload["name"] = str(settings["stationname"])
	if settings["latitude"] and settings["longitude"]:
		payload["lat"] = str(settings["latitude"])
		payload["long"] = str(settings["longitude"])
	if settings["altitude"]:
		payload["alt"] = str(settings["altitude"])
	return payload