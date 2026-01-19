import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  ButtonStyle,
  MessageComponentData,
} from "../types/discord";
import {
  embedResponse,
  errorResponse,
  updateResponse,
  createButtonRow,
} from "../utils/discord";
import { getOptionValue } from "../handlers/commands";

interface WeatherData {
  location: string;
  lat: number;
  lon: number;
  weeklyForecast: { day: string; high: number; low: number }[];
  todayForecast: {
    high: number;
    highTime: number;
    low: number;
    lowTime: number;
  };
}

const DAYS_OF_WEEK = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

async function getGeocode(
  zipCode: string,
): Promise<{ location: string; lat: number; lon: number } | null> {
  try {
    const url = `https://nominatim.openstreetmap.org/search?q=${zipCode}+United+States&format=json`;
    const response = await fetch(url, {
      headers: { "User-Agent": "MEGABOT/2.0" },
    });
    const data = (await response.json()) as any[];

    if (data.length === 0) {
      return null;
    }

    return {
      location: data[0].display_name,
      lat: parseFloat(data[0].lat),
      lon: parseFloat(data[0].lon),
    };
  } catch (error) {
    console.error("Geocode error:", error);
    return null;
  }
}

async function getWeatherForecast(
  lat: number,
  lon: number,
): Promise<{
  weekly: { day: string; high: number; low: number }[];
  today: { high: number; highTime: number; low: number; lowTime: number };
}> {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m&temperature_unit=fahrenheit`;
  const response = await fetch(url);
  const data = (await response.json()) as {
    hourly: { temperature_2m: number[] };
  };

  const temps = data.hourly.temperature_2m;

  // Get today's high/low
  const todayTemps = temps.slice(0, 24);
  const todayHigh = Math.max(...todayTemps);
  const todayLow = Math.min(...todayTemps);
  const todayHighTime = todayTemps.indexOf(todayHigh);
  const todayLowTime = todayTemps.indexOf(todayLow);

  // Get weekly high/lows
  const weekly: { day: string; high: number; low: number }[] = [];
  const today = new Date();

  for (let i = 0; i < 7; i++) {
    const dayTemps = temps.slice(i * 24, (i + 1) * 24);
    if (dayTemps.length === 0) break;

    const dayDate = new Date(today);
    dayDate.setDate(dayDate.getDate() + i);

    weekly.push({
      day: DAYS_OF_WEEK[dayDate.getDay()],
      high: Math.round(Math.max(...dayTemps)),
      low: Math.round(Math.min(...dayTemps)),
    });
  }

  return {
    weekly,
    today: {
      high: Math.round(todayHigh),
      highTime: todayHighTime,
      low: Math.round(todayLow),
      lowTime: todayLowTime,
    },
  };
}

function formatHour(hour: number): string {
  if (hour === 0) return "12 AM";
  if (hour === 12) return "12 PM";
  if (hour < 12) return `${hour} AM`;
  return `${hour - 12} PM`;
}

function encodeWeatherState(zipCode: string): string {
  return Buffer.from(zipCode).toString("base64");
}

function decodeWeatherState(encoded: string): string {
  return Buffer.from(encoded, "base64").toString("utf-8");
}

export async function handleWeather(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const zipCode = getOptionValue<string>(interaction, "zipcode")!;

  // Validate ZIP code
  if (!/^\d{5}$/.test(zipCode)) {
    return errorResponse(
      "Invalid ZIP code. Please enter a 5-digit US ZIP code.",
    );
  }

  // Get geocode
  const geocode = await getGeocode(zipCode);
  if (!geocode) {
    return errorResponse("Could not find location for that ZIP code.");
  }

  // Get weather
  const weather = await getWeatherForecast(geocode.lat, geocode.lon);

  // Build weekly forecast description
  let description = `**Location:** ${geocode.location.split(",").slice(0, 2).join(",")}\n\n__Weekly Forecast:__\n`;
  for (const day of weather.weekly) {
    description += `**${day.day}**: High ${day.high}° Low ${day.low}°\n`;
  }

  const encodedState = encodeWeatherState(zipCode);

  return embedResponse(
    {
      title: "☁️ Weather Forecast",
      description,
      color: 0xf2eef9,
    },
    false,
    [
      createButtonRow([
        {
          customId: `weather_today_${encodedState}`,
          label: "Today's Weather",
          style: ButtonStyle.PRIMARY,
        },
        {
          customId: `weather_weekly_${encodedState}`,
          label: "Weekly Forecast",
          style: ButtonStyle.SECONDARY,
        },
      ]),
    ],
  );
}

export async function handleWeatherComponent(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const data = interaction.data as MessageComponentData;
  const customId = data.custom_id;

  const parts = customId.split("_");
  const view = parts[1]; // 'today' or 'weekly'
  const encodedState = parts.slice(2).join("_");
  const zipCode = decodeWeatherState(encodedState);

  // Get geocode
  const geocode = await getGeocode(zipCode);
  if (!geocode) {
    return errorResponse("Could not find location.");
  }

  // Get weather
  const weather = await getWeatherForecast(geocode.lat, geocode.lon);

  let description: string;

  if (view === "today") {
    description = `**Location:** ${geocode.location.split(",").slice(0, 2).join(",")}\n\n__Daily Outlook:__\n`;
    description += `**High:** ${weather.today.high}° @ ${formatHour(weather.today.highTime)}\n`;
    description += `**Low:** ${weather.today.low}° @ ${formatHour(weather.today.lowTime)}`;
  } else {
    description = `**Location:** ${geocode.location.split(",").slice(0, 2).join(",")}\n\n__Weekly Forecast:__\n`;
    for (const day of weather.weekly) {
      description += `**${day.day}**: High ${day.high}° Low ${day.low}°\n`;
    }
  }

  return updateResponse(
    {
      title: view === "today" ? "☁️ Today's Weather" : "☁️ Weather Forecast",
      description,
      color: 0xf2eef9,
    },
    [
      createButtonRow([
        {
          customId: `weather_today_${encodedState}`,
          label: "Today's Weather",
          style: ButtonStyle.PRIMARY,
        },
        {
          customId: `weather_weekly_${encodedState}`,
          label: "Weekly Forecast",
          style: ButtonStyle.SECONDARY,
        },
      ]),
    ],
  );
}
