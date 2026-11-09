import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";

// Animated Kanye emoji from MEGACORD
const KANYE_EMOJI = "<a:kanyePls:1081048056058871808>";

export async function handleKanye(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  try {
    const response = await fetch("https://api.kanye.rest/");
    const data = (await response.json()) as { quote: string };

    return embedResponse({
      title: "Kanye Quote",
      description: `${KANYE_EMOJI}  “${data.quote}”`,
      color: Colors.GOLD,
    });
  } catch (error) {
    console.error("Kanye API error:", error);
    return errorResponse("Failed to get a Kanye quote. Try again later.");
  }
}
