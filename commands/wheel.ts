import {
  DiscordInteraction,
  InteractionResponse,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse } from "../utils/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { getBalance, addCoins, subtractCoins } from "../services/megacoin";

// Wheel multipliers matching Python: [0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2]
const WHEEL_OPTIONS = [0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2];

function spinWheel(): { multiplier: number; variant: number } {
  const multiplier =
    WHEEL_OPTIONS[Math.floor(Math.random() * WHEEL_OPTIONS.length)];
  const variant = Math.random() < 0.5 ? 1 : 2; // Random 1 or 2 for image variant
  return { multiplier, variant };
}

export async function handleWheel(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const wager = getOptionValue<number>(interaction, "wager")!;
  const user = getUser(interaction);

  // Validation (matches Python)
  if (wager < 0) {
    return embedResponse({
      title: "☸️ Spin the Wheel",
      description: "🤡 Nice try.",
      color: 0x9366cd,
    });
  }

  const balance = await getBalance(user.id);

  if (balance === 0) {
    return embedResponse({
      title: "☸️ Spin the Wheel",
      description: `You have 0 ${MEGACOIN_EMOJI}`,
      color: 0x9366cd,
    });
  }

  if (balance < wager) {
    return embedResponse({
      title: "☸️ Spin the Wheel",
      description: `You don't have ${wager} ${MEGACOIN_EMOJI}`,
      color: 0x9366cd,
    });
  }

  // Spin the wheel
  const { multiplier, variant } = spinWheel();
  const winnings = Math.floor(wager * multiplier);

  // Apply the bet
  await subtractCoins(user.id, user.username, wager);
  if (winnings > 0) {
    await addCoins(user.id, user.username, winnings);
  }
  const newBalance = await getBalance(user.id);

  // Use wheel result image from GitHub (matches Python)
  const imageUrl = `https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/${multiplier}-${variant}.jpg`;

  return embedResponse({
    title: "☸️ Spin the Wheel",
    description: `<@${user.id}> wagered ${wager} ${MEGACOIN_EMOJI} and **won ${winnings}** ${MEGACOIN_EMOJI}!`,
    color: 0x9366cd,
    thumbnail: { url: imageUrl },
    footer: { text: `Their balance is now ${newBalance}` },
  });
}
