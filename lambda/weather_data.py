import json
import datetime
import time

'''
 * Weather calculating algorithm from
 * https://github.com/Rogueadyn/SaintCoinach/blob/master/SaintCoinach/Xiv/WeatherRate.cs
''' 
# read file
with open('lambda/weather-data.json', 'r') as myfile:
    data = myfile.read()

WEATHER_DATA = json.loads(data)
EORZEA_HOUR = 175 * 1000
EORZEA_8_HOUR = 8 * 175 * 1000
EORZEA_DAY = 24 * 175 * 1000

now = datetime.datetime.now()
int_time = int(now.strftime("%H%M%S"))
change_interval = datetime.timedelta(hours=8)
poss_weathers = []
weather_rates = []



"""
You can update this method with an actual Weather API call. This will just look up a data object from a small
list in a file.
@param cityId the city name value's slot id, parsed from the resolved slot
@param date the date
@returns {Object} an object with highTemperature and lowTemperature fields, or an empty object

Right now this is using fake data until I can write the weather generator code that gets real data.

"""
def getWeather(cityId):
    if cityId in WEATHER_DATA:
        return WEATHER_DATA[cityId]

    return {}

e_hours_from_epoch = int_time/EORZEA_HOUR
e_days_from_epoch = int_time/EORZEA_DAY
inc = (int_time + 8 - (int_time % 8)) %24

def calculatetarget(from_time):
    unix = time.time()
    # Get Eorzea hour for weather start
    bell = unix / 175
    # Do the magic 'cause for calculations 16:00 is 0, 00:00 is 8 and 08:00 is 16
    increment = (int(bell + 8 - (bell % 8))) % 24

            #Take Eorzea days since unix epoch
    totalDays = int(unix / 4200)

    calcBase = (totalDays * 100) + increment

    step1 = (calcBase << 11) ^ calcBase
    step2 = (step1 >> 8) ^ step1

    return int(step2 % 100)

print(calculatetarget(inc))
