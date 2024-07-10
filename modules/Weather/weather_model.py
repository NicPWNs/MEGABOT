import requests


# Model for weather command
# Get todays weather for location
async def get_todays_temps(lat, long):
    # Only get temp right now and the time it will occur

    # Request API call for single day with lat & long
    request = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude="
        + str(lat)
        + "&longitude="
        + str(long)
        + "&hourly=temperature_2m&temperature_unit=fahrenheit&precipitation_unit=inch&forecast_days=1"
    ).json()

    # Get the temperature by hour for today (includes past hours of day)
    hourlyList = list(map(float, request["hourly"]["temperature_2m"]))

    # Variables to hold info
    dailyHigh = float(hourlyList[0])
    dailyLow = float(hourlyList[0])
    dailyHighTime = ""
    dailyLowTime = ""

    count = 0
    for i in hourlyList:
        if dailyHigh < i:
            dailyHigh = i
            dailyHighTime = count
        elif dailyLow > i:
            dailyLow = i
            dailyLowTime = count
        count += 1

    # Index: high, high time, low, low time
    dailyWeatherList = [dailyHigh, dailyHighTime, dailyLow, dailyLowTime]

    return dailyWeatherList


# Get 7 day daily high/lows for location
async def get_weekly_temps(lat, long):
    dailyTemps = []

    # Get weather data
    request = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude="
        + str(lat)
        + "&longitude="
        + str(long)
        + "&hourly=temperature_2m&temperature_unit=fahrenheit"
    ).json()

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


# Get 7 day forecast for precipitation - not implemented
async def get_precip(lat, long):
    precipChance = []

    return precipChance


# Get geocode from ZIP code
async def get_geocode(zipCode):

    # https://nominatim.openstreetmap.org/search?q=20024+United+States&format=json
    url = (
        "https://nominatim.openstreetmap.org/search?q="
        + str(zipCode)
        + "+United+States&format=json"
    )

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
    }

    response = requests.get(
        url=url,
        headers=headers,
    ).json()

    latitude = round(float(response[0]["lat"]), 2)
    longitude = round(float(response[0]["lon"]), 2)
    location = response[0]["display_name"]

    return [location, latitude, longitude]
