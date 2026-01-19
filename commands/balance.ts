import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse, textResponse } from "../utils/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { getBalance } from "../services/megacoin";

export async function handleBalance(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  // Get the target user (if specified) or the command user
  const targetUserId = getOptionValue<string>(interaction, "user");
  const commandUser = getUser(interaction);

  const userId = targetUserId || commandUser.id;
  const balance = await getBalance(userId);

  if (targetUserId) {
    return textResponse(
      `<@${targetUserId}>'s balance is **${balance}** ${MEGACOIN_EMOJI}`,
    );
  }

  return textResponse(
    `<@${commandUser.id}>'s balance is **${balance}** ${MEGACOIN_EMOJI}`,
  );
}
