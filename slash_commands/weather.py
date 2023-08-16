from datetime import datetime
import re
import discord
import requests

from modules.weather_info import get_daily_temps

# Display 7 day weather forecast for zip code
async def weather_forecast(ctx, zipCode):

   # Zipcode Validation
   if not re.match('^[0-9]{5}$', zipCode):
      embed = discord.Embed(
         color=0x9366cd, title="Weather Forecast", description="Invalid Zipcode.")
      await ctx.respond(embed=embed)
      return

   # Finding geocode from zip code
   request = requests.get('https://nominatim.openstreetmap.org/search?q=' + str(zipCode) + '+United+States&format=json').json()

   latitude = round(float(request[0]["lat"]), 2)
   longitude = round(float(request[0]["lon"]), 2)
   location = request[0]["display_name"]

   # Get daily high/lows
   dailyTemps = await get_daily_temps(latitude, longitude)

   # Output weekly temperature forecast message

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
   forecastInfo = "Location: " + location + "\nWeekly Forecast:"
   for i in range(7):
      forecastInfo += "\n" + displayDays[i] + ": High " + str(dailyTemps[0][i]) + ", Low " + str(dailyTemps[1][i])

   return forecastInfo
