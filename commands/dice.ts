import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse } from "../utils/discord";

const DICE_FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];

export async function handleDice(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const roll = Math.floor(Math.random() * 6) + 1;
  const face = DICE_FACES[roll - 1];

  return embedResponse({
    title: "🎲 Dice Roll",
    description: `${face} You rolled a **${roll}**!`,
    color: Colors.PURPLE,
  });
}
