import {
  DiscordInteraction,
  InteractionResponse,
  ApplicationCommandData,
} from "../types/discord";
import { errorResponse } from "../utils/discord";

// Import command handlers
import { handlePing } from "../commands/ping";
import { handleVersion } from "../commands/version";
import { handleCoin } from "../commands/coin";
import { handleDice } from "../commands/dice";
import { handleBless } from "../commands/bless";
import { handleKanye } from "../commands/kanye";
import { handleMath } from "../commands/math";
import { handlePoll } from "../commands/poll";
import { handleBalance } from "../commands/balance";
import { handleBank } from "../commands/bank";
import { handlePay } from "../commands/pay";
import { handlePayout } from "../commands/payout";
import { handleBlackjack } from "../commands/blackjack";
import { handleDouble } from "../commands/double";
import { handleWheel } from "../commands/wheel";
import { handleStreak } from "../commands/streak";
import { handleWeather } from "../commands/weather";
import { handleStock } from "../commands/stock";
import { handleNasa } from "../commands/nasa";
import { handleMc } from "../commands/mc";
import { handlePhoto } from "../commands/photo";
import { handleBug } from "../commands/bug";
import { handleFeature } from "../commands/feature";
import { handleEmote } from "../commands/emote";

// Command handler map
const commandHandlers: Record<
  string,
  (interaction: DiscordInteraction) => Promise<InteractionResponse>
> = {
  ping: handlePing,
  version: handleVersion,
  coin: handleCoin,
  dice: handleDice,
  bless: handleBless,
  kanye: handleKanye,
  math: handleMath,
  poll: handlePoll,
  balance: handleBalance,
  bank: handleBank,
  pay: handlePay,
  payout: handlePayout,
  blackjack: handleBlackjack,
  double: handleDouble,
  wheel: handleWheel,
  streak: handleStreak,
  weather: handleWeather,
  stock: handleStock,
  nasa: handleNasa,
  mc: handleMc,
  photo: handlePhoto,
  bug: handleBug,
  feature: handleFeature,
  emote: handleEmote,
};

/**
 * Handle slash command interactions
 */
export async function handleSlashCommand(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const data = interaction.data as ApplicationCommandData;
  const commandName = data.name;

  console.log(`Handling command: ${commandName}`);

  const handler = commandHandlers[commandName];

  if (!handler) {
    console.warn(`Unknown command: ${commandName}`);
    return errorResponse(`Unknown command: ${commandName}`);
  }

  try {
    return await handler(interaction);
  } catch (error) {
    console.error(`Error in command ${commandName}:`, error);
    return errorResponse("An error occurred while processing this command.");
  }
}

/**
 * Get command option value by name
 */
export function getOptionValue<T>(
  interaction: DiscordInteraction,
  name: string,
): T | undefined {
  const data = interaction.data as ApplicationCommandData;
  const option = data.options?.find((opt) => opt.name === name);
  return option?.value as T | undefined;
}

/**
 * Get the user from the interaction (works for both guild and DM)
 */
export function getUser(interaction: DiscordInteraction) {
  return interaction.member?.user || interaction.user!;
}

/**
 * Get a resolved user from the interaction by user ID
 * Discord includes resolved user data for user options
 */
export function getResolvedUser(
  interaction: DiscordInteraction,
  userId: string,
) {
  const data = interaction.data as ApplicationCommandData;
  return data.resolved?.users?.[userId];
}
