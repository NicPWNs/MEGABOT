import {
  DiscordInteraction,
  InteractionResponse,
  InteractionResponseType,
} from "../types/discord";
import { getOptionValue } from "../handlers/commands";

const NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"];
const DEFAULT_DURATION_HOURS = 24;

/**
 * Create a native Discord poll. Discord tracks votes (one per user),
 * shows live results, and closes the poll when the duration ends.
 */
export async function handlePoll(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const question = getOptionValue<string>(interaction, "question")!;
  const hours =
    getOptionValue<number>(interaction, "hours") ?? DEFAULT_DURATION_HOURS;

  const options = Array.from({ length: 9 }, (_, i) =>
    getOptionValue<string>(interaction, `option${i + 1}`),
  ).filter((opt): opt is string => opt !== undefined);

  return {
    type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    data: {
      poll: {
        question: { text: question },
        answers: options.map((text, index) => ({
          poll_media: { text, emoji: { name: NUMBER_EMOJIS[index] } },
        })),
        duration: hours,
        allow_multiselect: false,
        layout_type: 1,
      },
    },
  };
}
