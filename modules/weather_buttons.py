import discord
from discord.ui.item import Item

from slash_commands.weather import weather_forecast

# Weather UI Components
class WeatherUI(discord.ui.View):
   def __init__(self, ctx, zipcode, *items: Item, timeout: float, disable_on_timeout: bool = False):
      super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)

      self.ctx = ctx
      self.zipcode = zipcode

   # Disable buttons
   async def on_timeout(self):
      self.disable_all_items()

   # Todays forecast button
   @discord.ui.button(label="Todays Weather", style=discord.ButtonStyle.primary)
   async def todays_weather(self, button, interaction):
      embed = discord.Embed(color=0xf2eef9, title="☁️  Todays Weather", description="Not Currently Implemented. Sorry.")
      await interaction.response.edit_message(embed=embed)

   # Weekly forecast button
   @discord.ui.button(label="Weekly Forecast", style=discord.ButtonStyle.primary)
   async def weekly_weather(self, button: discord.ui.Button, interaction: discord.Interaction):
      weeklyForecastInfo = await weather_forecast(self.ctx, self.zipcode)
      embed = discord.Embed(
         color=0xf2eef9, title="☁️  Weather Forecast", description=weeklyForecastInfo)
      await interaction.response.edit_message(embed=embed)
