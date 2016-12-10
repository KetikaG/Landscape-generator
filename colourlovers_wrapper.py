## Initial skecthes on building an API wrapper to get color palettes (Colourlovers API)

# Imports
from urllib2 import Request, urlopen, URLError

# API wrapper
class ColourLovers(object):
	'''
	ColourLovers API python wrapper
	'''
	def __init__(self):
		self.__API_URL        = "http://www.colourlovers.com/api/"
		
		self.__API_REQUESTS   = {"colors":set({"new","top","random"}),
								 "palettes":set({"new","top","random"}),
								 "patterns":set({"new","top","random"}),
								 "lovers":set({"new","top"}),
								 "stats":set({"colors", "palettes", "patterns", "lovers"})}
		
		self.__API_PARAMETRES = {"colors":set({"lover","hueRange","briRange","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "palettes":set({"lover","hueOption","hex","hex_logic","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback","showPaletteWidths"}),
								 "patterns":set({"lover","hueOption","hex","hex_logic","keywords","keywordExact","orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "lovers":set({"orderCol","sortBy","numResults","resultOffset","format","jsonCallback"}),
								 "stats":set({"format","jsonCallback"})}
		
		self.__API_ADD_PARAM  = ["&","="]

		self.__API_COLORS     = "colors"
		self.__API_PALETTES   = "palettes" 
		self.__API_PATTERNS   = "patterns"
		self.__API_LOVERS     = "lovers"
		self.__API_STATS      = "stats"

	# Public methods
	def search_colors(self, **kwargs):
		self.__search(self.__API_COLORS, **kwargs)
		pass

	def search_palettes(self, **kwargs):
		self.__search(self.__API_PALETTES, **kwargs)
		pass

	def search_patterns(self, **kwargs):
		self.__search(self.__API_PATTERNS, **kwargs)
		pass

	def search_lovers(self, **kwargs):
		self.__search(self.__API_LOVERS, **kwargs)
		pass

	def search_stats(self, **kwargs):
		self.__search(self.__API_STATS, **kwargs)
		pass



	# Private methods
	def __search(self, searchterm, **kwargs):
		try: 
			self.__check_args(searchterm, **kwargs)
		except ValueError as e:
			print(e)

		xml_response = self.__request(searchterm, **kwargs)
			
	def __check_args(self, searchterm, **kwargs):
		if searchterm not in self.__API_REQUESTS.keys():
			raise ValueError("Unsupported search: "+searchterm)

		elif kwargs is not None:
			# Look for invalid arguments
			invalid_parameters = set(kwargs.keys())-self.__API_PARAMETRES[searchterm]
			if invalid_parameters:
				raise ValueError("Unsupported search argument/s: "+', '.join(invalid_parameters))

			# Look for invalid argument value types
			types = [(i,type(value)) for (i,value) in enumerate(kwargs.values())]
			for parameter_type in types:
				if parameter_type[1] not in [list,str,int]:
					raise ValueError("Unsupported argument value type "+str(parameter_type))
				# If the argument value is a list, the type of all the elements in the list should be
				# a valid type and the same type for all the values
				elif parameter_type[1]==list:
					parameter_values_types = [type(parameter_value) for parameter_value in kwargs.values()[parameter_type[0]]]
					type_selector = parameter_values_types[0] # Select the type of the first value in list as the parameter type
															  # and look for inconsistencies or invalid types
					if type_selector not in [str,int]:
						raise ValueError("Unsupported value type in argument "+str(kwargs.keys()[parameter_type[0]]))
					for parameter_value_type in parameter_values_types:
						if parameter_value_type != type_selector:
							raise ValueError("Inconsistent value types in argument "+str(kwargs.keys()[parameter_type[0]]))
		else:
			return True

	def __request(self, searchterm, **kwargs):
		# build API request
		api_request_url = self.__API_URL+searchterm

		for argument in kwargs.keys():
			# build API parameter specification string
			if type(kwargs[argument])==list:
				values = ','.join([str(value) for value in kwargs[argument]])
			else:
				values = str(kwargs[argument])
			additional_parameter = self.__API_ADD_PARAM[0]+argument+self.__API_ADD_PARAM[1]+values
			# add parameter to API request
			api_request_url+=additional_parameter

		# HTTP API request
		req = Request(api_request_url, headers={'User-Agent' : "Magic Browser"})

		# Make request and read response
		try:
			response = urlopen(req)
			data = response.read()
			return data
		except URLError, e:
			print 'Error', e
			return None