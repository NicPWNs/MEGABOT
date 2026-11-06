import {
  DiscordInteraction,
  InteractionResponse,
  MessageComponentData,
} from "../types/discord";
import { errorResponse } from "../utils/discord";
import { handleBlackjackComponent } from "../commands/blackjack";
import { handleWeatherComponent } from "../commands/weather";

/**
 * Handle component interactions (buttons, select menus)
 */
export async function handleComponentInteraction(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const data = interaction.data as MessageComponentData;
  const customId = data.custom_id;

  console.log(`Handling component interaction: ${customId}`);

  // Route based on custom_id prefix
  if (customId.startsWith("blackjack_")) {
    return await handleBlackjackComponent(interaction);
  }

  if (customId.startsWith("weather_")) {
    return await handleWeatherComponent(interaction);
  }

  console.warn(`Unknown component interaction: ${customId}`);
  return errorResponse("Unknown interaction");
}
