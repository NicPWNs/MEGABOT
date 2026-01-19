import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse } from "../utils/discord";

export async function handleCoin(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const result = Math.random() < 0.5 ? "Heads" : "Tails";
  const emoji = result === "Heads" ? "🪙" : "🔄";

  return embedResponse({
    title: `${emoji} Coin Flip`,
    description: `**${result}!**`,
    color: Colors.GOLD,
  });
}
