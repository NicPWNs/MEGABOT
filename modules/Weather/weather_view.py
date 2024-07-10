import discord
from discord.ui.item import Item


# Weather View UI Components
class WeatherUI(discord.ui.View):
    def __init__(
        self,
        ctx,
        weeklyForecast,
        todaysForecast,
        *items: Item,
        timeout: float,
        disable_on_timeout: bool = False
    ):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)

        self.ctx = ctx
        self.weeklyForecast = weeklyForecast
        self.todaysForecast = todaysForecast

        # print(self.func)

    # Disable buttons
    async def on_timeout(self):
        self.disable_all_items()

    # Todays forecast button
    @discord.ui.button(label="Todays Weather", style=discord.ButtonStyle.primary)
    async def todays_weather(self, button, interaction):
        embed = discord.Embed(
            color=0xF2EEF9, title="☁️  Todays Weather", description=self.todaysForecast
        )
        await interaction.response.edit_message(embed=embed)

    # Weekly forecast button
    @discord.ui.button(label="Weekly Forecast", style=discord.ButtonStyle.primary)
    async def weekly_weather(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        embed = discord.Embed(
            color=0xF2EEF9, title="☁️  Weather Forecast", description=self.weeklyForecast
        )
        await interaction.response.edit_message(embed=embed)


async def invalidZipCode(ctx):
    embed = discord.Embed(
        color=0x9366CD, title="Weather Forecast", description="Invalid Zipcode."
    )
    await ctx.respond(embed=embed)
    return
