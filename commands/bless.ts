import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse } from "../utils/discord";

export async function handleBless(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  return embedResponse({
    title: "✨ The mess has been blessed!",
    color: Colors.GOLD,
  });
}
