import {
  DiscordInteraction,
  InteractionResponse,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse } from "../utils/discord";
import { getOptionValue, getUser, getResolvedUser } from "../handlers/commands";
import { addCoins } from "../services/megacoin";
import { userHasRoleByName } from "../utils/discord-api";

export async function handlePayout(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const user = getUser(interaction);
  const guildId = interaction.guild_id;

  // Check if user has MEGAPAYERS role (matches Python)
  if (!guildId) {
    return embedResponse({
      title: "🏆 Payout",
      description: "🤡 This command can only be used in a server.",
      color: 0xffcd4c,
    });
  }

  const hasPerm = await userHasRoleByName(guildId, user.id, "MEGAPAYERS");
  if (!hasPerm) {
    return embedResponse({
      title: "🏆 Payout",
      description: `🤡 Nice try <@${user.id}>.`,
      color: 0xffcd4c,
    });
  }

  const targetUserId = getOptionValue<string>(interaction, "user")!;
  const amount = getOptionValue<number>(interaction, "amount")!;
  const message = getOptionValue<string>(interaction, "message")!;

  // Get target user's info from resolved data
  const targetUser = getResolvedUser(interaction, targetUserId);
  const targetUsername = targetUser?.username || "Unknown";
  const targetAvatar = targetUser?.avatar
    ? `https://cdn.discordapp.com/avatars/${targetUserId}/${targetUser.avatar}.png`
    : undefined;

  // Add coins to target user
  await addCoins(targetUserId, targetUsername, amount);

  return embedResponse({
    title: "🏆 Payout",
    description: `**<@${targetUserId}> Earned ${amount} ${MEGACOIN_EMOJI}.**\n\n${message}`,
    color: 0xffcd4c,
    thumbnail: targetAvatar ? { url: targetAvatar } : undefined,
  });
}
