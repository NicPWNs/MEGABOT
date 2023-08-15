import requests

# Module for obtaining weather information

# Get todays weather for location
async def todays_weather(lat, long):
   dailyWeatherList = []

   return dailyWeatherList

# Get 7 day daily high/lows for location
async def get_daily_temps(lat, long):
   dailyTemps = []

   # Get weather data
   request = requests.get(
      'https://api.open-meteo.com/v1/forecast?latitude=' + str(lat) + '&longitude=' + str(long) + '&hourly=temperature_2m&temperature_unit=fahrenheit').json()

   # Hold high/low temps
   highTempList = []
   lowTempList = []

   # Get the temperature by hour for next 7 days (168 hours index)
   hourlyList = list(map(float, request["hourly"]["temperature_2m"]))

   # Get daily highs/lows
   hourCount = 0
   dailyTempHigh = float(hourlyList[0])
   dailyTempLow = float(hourlyList[0])
   for i in hourlyList:
      if dailyTempHigh < i:
         dailyTempHigh = i
      elif dailyTempLow > i:
         dailyTempLow = i

      hourCount += 1
      # Reset everything for next day
      if hourCount == 24:
         highTempList.append(dailyTempHigh)
         lowTempList.append(dailyTempLow)
         dailyTempHigh = i
         dailyTempLow = i
         hourCount = 0

   dailyTemps.append(highTempList)
   dailyTemps.append(lowTempList)

   return dailyTemps

# Get 7 day forecast for preciptation
async def get_precip(lat, long):
   precipChance = []

   return precipChance