import {
  DiscordInteraction,
  InteractionResponse,
  MessageComponentData,
  InteractionResponseType,
} from "../types/discord";
import { errorResponse, textResponse } from "../utils/discord";
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

  if (customId.startsWith("poll_vote_")) {
    return handlePollVote(interaction);
  }

  console.warn(`Unknown component interaction: ${customId}`);
  return errorResponse("Unknown interaction");
}

/**
 * Handle poll vote button clicks
 * Note: This is a simple acknowledgement - serverless can't track votes persistently
 * without a database. For full poll functionality, use Discord's native polls.
 */
function handlePollVote(interaction: DiscordInteraction): InteractionResponse {
  const data = interaction.data as MessageComponentData;
  const optionIndex = parseInt(data.custom_id.replace("poll_vote_", ""), 10);
  const NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"];
  const emoji = NUMBER_EMOJIS[optionIndex] || "?";

  const user = interaction.member?.user || interaction.user!;

  // Ephemeral response to acknowledge their vote
  return {
    type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    data: {
      content: `${user.username} voted for option ${emoji}!`,
      flags: 0, // Public so others can see the vote
    },
  };
}
