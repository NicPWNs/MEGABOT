import {
  DiscordInteraction,
  InteractionResponse,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse } from "../utils/discord";
import { getOptionValue, getUser, getResolvedUser } from "../handlers/commands";
import { getBalance, transferCoins } from "../services/megacoin";
import { sendDM } from "../utils/discord-api";

export async function handlePay(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const targetUserId = getOptionValue<string>(interaction, "user")!;
  const amount = getOptionValue<number>(interaction, "amount")!;
  const user = getUser(interaction);

  // Can't pay negative or zero (matches Python)
  if (amount < 0) {
    return embedResponse({
      title: "💸 Payment",
      description: "🤡 Nice try.",
      color: 0xa7d38a,
    });
  }

  // Check balance
  const balance = await getBalance(user.id);

  if (balance === 0) {
    return embedResponse({
      title: "💸 Payment",
      description: `You have 0 ${MEGACOIN_EMOJI}`,
      color: 0xa7d38a,
    });
  }

  if (balance < amount) {
    return embedResponse({
      title: "💸 Payment",
      description: `You don't have ${amount} ${MEGACOIN_EMOJI}`,
      color: 0xa7d38a,
    });
  }

  // Get target user's info from resolved data
  const targetUser = getResolvedUser(interaction, targetUserId);
  const targetUsername = targetUser?.username || "Unknown";

  // Transfer
  const result = await transferCoins(
    user.id,
    user.username,
    targetUserId,
    targetUsername,
    amount,
  );

  if (!result.success) {
    return embedResponse({
      title: "💸 Payment",
      description: result.message,
      color: 0xa7d38a,
    });
  }

  // Send DM to recipient (matches Python)
  await sendDM(
    targetUserId,
    `💸 You received ${amount} ${MEGACOIN_EMOJI} from <@${user.id}>`,
  );

  return embedResponse({
    title: "💸 Payment",
    description: `<@${user.id}> sent ${amount} ${MEGACOIN_EMOJI} to <@${targetUserId}>`,
    color: 0xa7d38a,
  });
}
