import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse } from "../utils/discord";
import { getLeaderboard } from "../services/megacoin";

export async function handleBank(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const leaderboard = await getLeaderboard();

  if (leaderboard.length === 0) {
    return embedResponse({
      title: "💰 MEGACOIN LEADERBOARD",
      description: "No one has any MEGACOIN yet!",
      color: Colors.BLUE,
    });
  }

  let description = "";
  leaderboard.forEach((user, index) => {
    const medal =
      index === 0
        ? "🥇"
        : index === 1
          ? "🥈"
          : index === 2
            ? "🥉"
            : `${index + 1}.`;
    description += `${medal} <@${user.id}> with ${user.coins} ${MEGACOIN_EMOJI}\n`;
  });

  return embedResponse({
    title: "💰 MEGACOIN LEADERBOARD",
    description,
    color: Colors.BLUE,
  });
}
