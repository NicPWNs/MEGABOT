from datetime import datetime
import re
from time import strftime
from modules.Weather.weather_model import get_geocode, get_todays_temps
from modules.Weather.weather_view import WeatherUI, invalidZipCode
from modules.Weather.weather_model import get_weekly_temps

# Acts as Controller for weather command
# weather_view & weather_model

# Main function
async def weather(ctx, zipCode):

   # Validate zipCode
   if not re.match(r"^[0-9]{5}$", zipCode):
      invalidZipCode(ctx)

   # Get geocode - [location, lat, long]
   geocode = await get_geocode(zipCode)

   # Get Weekly & Daily Forecast
   ### Could go the other route and pass functions into the View in order to not run both here, 
   ### but will cause coroutine error trying to run again - need to find solution
   weeklyForecastMessage = await weekly_forecast(geocode)
   todaysForecastMessage = await todays_forecast(geocode)

   # Instantiate View UI
   weatherView = WeatherUI(ctx, weeklyForecastMessage, todaysForecastMessage, timeout=30)

   return weatherView

# Return 7 day weather forecast for zip code
async def weekly_forecast(geocode):

   # Get daily high/lows
   dailyTemps = await get_weekly_temps(geocode[1], geocode[2])

   # Hold days of the week
   days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
   displayDays = []

   # Get next 7 days of week
   dayCount = datetime.now().weekday()
   for i in range(7):

      displayDays.append(days_of_week[dayCount])

      dayCount += 1
      if dayCount == 7:
         dayCount = 0

   # Weather info display
   forecastInfo = "**Location:** " + geocode[0] + "\n\n__Weekly Forecast:__"
   for i in range(7):
      forecastInfo += "\n**" + displayDays[i] + "**: High " + str(dailyTemps[0][i]) + "°  Low " + str(dailyTemps[1][i]) + "°"

   return forecastInfo

# Return todays weather outlook
async def todays_forecast(geocode):

   # Get todays high & low
   # index returned: high, high time, low, low time
   todayTemps = await get_todays_temps(geocode[1], geocode[2])

   # Converting to 12 hour format manually
   highHour = await twelve_hour_format(todayTemps[1])
   lowHour = await twelve_hour_format(todayTemps[3])

   # Weather info display
   forecastInfo = "**Location:** " + geocode[0] + "\n\n__Daily Outlook:__"
   forecastInfo += "\n** High: **" + str(todayTemps[0]) + "° @ " + highHour
   forecastInfo += "\n** Low: **" + str(todayTemps[2]) + "° @ " + lowHour

   return forecastInfo

# Convert to 12 hour format String
async def twelve_hour_format(hour):
   if hour == 0:
      return "12:00 AM"
   elif hour < 12:
      return f"{hour} AM"
   elif hour == 12:
      return "12:00 PM"
   else:
      return f"{hour - 12} PM"