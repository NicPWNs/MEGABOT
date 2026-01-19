import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { getBalance, addCoins, subtractCoins } from "../services/megacoin";

export async function handleDouble(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const wager = getOptionValue<number>(interaction, "wager")!;
  const user = getUser(interaction);

  // Validation
  if (wager <= 0) {
    return embedResponse({
      title: "⚖️ Double or Nothing",
      description: "🤡 Nice try.",
      color: Colors.PURPLE,
    });
  }

  const balance = await getBalance(user.id);

  if (balance === 0) {
    return embedResponse({
      title: "⚖️ Double or Nothing",
      description: `You have 0 ${MEGACOIN_EMOJI}`,
      color: Colors.PURPLE,
    });
  }

  if (balance < wager) {
    return embedResponse({
      title: "⚖️ Double or Nothing",
      description: `You don't have ${wager} ${MEGACOIN_EMOJI}`,
      color: Colors.PURPLE,
    });
  }

  // 50/50 chance
  const win = Math.random() < 0.5;

  if (win) {
    await addCoins(user.id, user.username, wager);
    const newBalance = await getBalance(user.id);

    return embedResponse({
      title: "⚖️ Double or Nothing",
      description: `<@${user.id}> wagered ${wager} ${MEGACOIN_EMOJI} and **doubled it!** 🎉`,
      color: Colors.GREEN,
      thumbnail: {
        url: "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/win.png",
      },
      footer: { text: `Balance: ${newBalance}` },
    });
  } else {
    await subtractCoins(user.id, user.username, wager);
    const newBalance = await getBalance(user.id);

    return embedResponse({
      title: "⚖️ Double or Nothing",
      description: `<@${user.id}> wagered ${wager} ${MEGACOIN_EMOJI} and **lost it!** 😢`,
      color: Colors.RED,
      thumbnail: {
        url: "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/lose.png",
      },
      footer: { text: `Balance: ${newBalance}` },
    });
  }
}
