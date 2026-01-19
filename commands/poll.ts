import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  ButtonStyle,
} from "../types/discord";
import { embedResponse, createButtonRow } from "../utils/discord";
import { getOptionValue } from "../handlers/commands";

const NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"];

export async function handlePoll(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const question = getOptionValue<string>(interaction, "question")!;
  const options: (string | undefined)[] = [
    getOptionValue<string>(interaction, "option1"),
    getOptionValue<string>(interaction, "option2"),
    getOptionValue<string>(interaction, "option3"),
    getOptionValue<string>(interaction, "option4"),
    getOptionValue<string>(interaction, "option5"),
    getOptionValue<string>(interaction, "option6"),
    getOptionValue<string>(interaction, "option7"),
    getOptionValue<string>(interaction, "option8"),
    getOptionValue<string>(interaction, "option9"),
  ];

  // Filter out undefined options
  const validOptions = options.filter(
    (opt): opt is string => opt !== undefined,
  );

  // Build the description with numbered options
  let description = "";
  validOptions.forEach((option, index) => {
    description += `\n${NUMBER_EMOJIS[index]}  ${option}`;
  });

  // Create button rows for voting (max 5 buttons per row)
  const components: ReturnType<typeof createButtonRow>[] = [];

  // First row (up to 5 options)
  const firstRowButtons = validOptions.slice(0, 5).map((_, index) => ({
    customId: `poll_vote_${index}`,
    label: NUMBER_EMOJIS[index],
    style: ButtonStyle.SECONDARY,
  }));
  if (firstRowButtons.length > 0) {
    components.push(createButtonRow(firstRowButtons));
  }

  // Second row (options 6-9)
  const secondRowButtons = validOptions.slice(5, 9).map((_, index) => ({
    customId: `poll_vote_${index + 5}`,
    label: NUMBER_EMOJIS[index + 5],
    style: ButtonStyle.SECONDARY,
  }));
  if (secondRowButtons.length > 0) {
    components.push(createButtonRow(secondRowButtons));
  }

  return {
    type: 4,
    data: {
      embeds: [
        {
          title: `🗳️ Poll: ${question}`,
          description: description + "\n\n*Click a button to vote!*",
          color: Colors.YELLOW,
        },
      ],
      components,
    },
  };
}
