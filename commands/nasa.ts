import { DiscordInteraction, InteractionResponse } from "../types/discord";
import { embedResponse, errorResponse, textResponse } from "../utils/discord";
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
    const data = (await response.json()) as NasaApodResponse;

    let content = data.url;

    if (showDetails) {
      content += `\n\n**${data.title}**\n${data.explanation}`;
    }

    return textResponse(content);
  } catch (error) {
    console.error("NASA API error:", error);
    return errorResponse(
      "Failed to fetch NASA photo of the day. Please try again later.",
    );
  }
}
