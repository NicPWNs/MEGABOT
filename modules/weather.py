import requests

# Module to handle obtaining weather information

# get todays weather for location
async def todays_weather(lat, long):
   dailyWeatherList = []

   return dailyWeatherList

# NOT IMPLEMENTED - return list for 7 day forecast of high temps
async def get_high_temps(lat, long):
   highTempList = []
    
   return highTempList
    
# NOT IMPLEMENTED - return list for 7 day forecast of low temps
async def get_low_temps(lat, long):
   lowTempList = []

   return lowTempList

# return list of both high and low lists
async def get_daily_temps(lat, long):
   dailyTemps = []

      # get weather data
   request = requests.get(
      'https://api.open-meteo.com/v1/forecast?latitude=' + str(lat) + '&longitude=' + str(long) + '&hourly=temperature_2m&temperature_unit=fahrenheit').json()

   # hold high/low temps
   highTempList = []
   lowTempList = []

   # Get the temperature by hour for next 7 days (168 hours/index)
   hourlyList = list(map(float, request["hourly"]["temperature_2m"]))

   # iterate over hourlyList
   hourCount = 0
   dailyTempHigh = float(hourlyList[0])
   dailyTempLow = float(hourlyList[0])
   for i in hourlyList:
      if dailyTempHigh < i:
         dailyTempHigh = i
      elif dailyTempLow > i:
         dailyTempLow = i
   
      hourCount += 1
      # reset everything for next day
      if hourCount == 24:
         highTempList.append(dailyTempHigh)
         lowTempList.append(dailyTempLow)
         dailyTempHigh = i
         dailyTempLow = i
         hourCount = 0

   dailyTemps.append(highTempList)
   dailyTemps.append(lowTempList)

   return dailyTemps

# get 7 day forecast for preciptation
async def get_precip(lat, long):
   precipChance = []

   return precipChance
