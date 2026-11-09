import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getOptionValue } from "../handlers/commands";

interface NasaApodResponse {
  url: string;
  title: string;
  explanation: string;
  media_type: string;
}

export async function handleNasa(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const showDetails = getOptionValue<boolean>(interaction, "details");
  const apiKey = process.env.NASA_KEY || "DEMO_KEY";

  try {
    const url = `https://api.nasa.gov/planetary/apod?api_key=${apiKey}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error(`NASA API returned ${response.status}`);
    const data = (await response.json()) as NasaApodResponse;

    const description = showDetails
      ? `${data.explanation}${data.media_type === "image" ? "" : `\n\n[Open today's media](${data.url})`}`
      : data.media_type === "image"
        ? undefined
        : `[Open today's media](${data.url})`;

    return embedResponse({
      title: data.title || "NASA Astronomy Picture of the Day",
      description,
      color: Colors.BLUE,
      image: data.media_type === "image" ? { url: data.url } : undefined,
    });
  } catch (error) {
    console.error("NASA API error:", error);
    return errorResponse(
      "Failed to fetch NASA photo of the day. Please try again later.",
    );
  }
}
