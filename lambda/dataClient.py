import json

# read file
with open('game-data.json', 'r') as myfile:
    data = myfile.read()

WEATHER_DATA = json.loads(data)

"""
You can update this method with an actual Weather API call. This will just look up a data object from a small
list in a file.
@param cityId the city name value's slot id, parsed from the resolved slot
@param date the date
@returns {Object} an object with highTemperature and lowTemperature fields, or an empty object
"""
def getData(cityId):
    if cityId and cityId in WEATHER_DATA:
        return WEATHER_DATA[cityId]

    return {}