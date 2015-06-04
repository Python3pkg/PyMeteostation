from ConfigParser import SafeConfigParser
from sys import exit

def getSettings(fileName):   # returns settings dictionary made of config file
	settings = {}
	parser = SafeConfigParser()
	try:
		parser.read(fileName)
	except Exception, e:
		exit("Unable to load configuration file. Error: "+str(e))

	raw_settings = {}								# load configuration from file to variable
	for section in parser.sections():
		raw_settings[section] = {}
		for option in parser.options(section):
			raw_settings[section][option] = parser.get(section,option)

	requiredSettings = {"Meteostation": ["upload_interval", "measurement_interval"], "I2C_Bus": ["port","devices"]}

	for section in requiredSettings.keys():			# check if required sections and options are configured
		if section in raw_settings.keys():
			for option in requiredSettings[section]:
				if not option in raw_settings[section].keys():
					exit("Unable to find \'%s\' option in \'%s\' section." % (option,section))
		else:
			exit("Unable to find \'%s\' section" % (section))

	for option in raw_settings["Meteostation"].keys():
		try:
			settings[option] = float(raw_settings["Meteostation"][option])
		except:
			settings[option] = raw_settings["Meteostation"][option]
	
	settings["I2C_configuration"] = getI2CConfig(raw_settings,"I2C_Bus")
	return settings

def getI2CConfig(settings,section): # generates I2C configuration from configuration file
	result = {"port": int(settings[section]["port"]), "bus": []}
	devices = getOptionList(settings[section]["devices"])

	for device in devices:
		result["bus"].append(getDeviceConfig(settings,device))
	return result

def getDeviceConfig(settings,section):	# recursively generates I2C configuration from configuration file
	result = {}
	for option in settings[section].keys():
		if option == "children":
			children = getOptionList(settings[section][option])
			result[option] = []
			for child in children:
				result[option].append(getDeviceConfig(settings,child))
		elif option == "address":
			result[option] = int(settings[section][option],base=16)
		elif option == "channel":
			result[option] = int(settings[section][option])
		else:
			result[option] = settings[section][option]
	return result

def getOptionList(string):
	lastPosition = 0
	optionList = []
	for letterPos in range(len(string)):
		if string[letterPos] == ";":
			optionList.append(string[lastPosition:letterPos])
			lastPosition = letterPos+1
	if lastPosition < len(string):
		optionList.append(string[lastPosition:len(string)])
	return optionList