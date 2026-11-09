import { DiscordInteraction, InteractionResponse } from "../types/discord";
import { COLOR_PALETTE } from "../types/commands";
import { getOptionValue, getUser } from "../handlers/commands";
import { embedResponse, errorResponse } from "../utils/discord";
import { setMemberColor } from "../utils/discord-api";

export async function handleColor(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const guildId = interaction.guild_id;
  const user = getUser(interaction);
  if (!guildId || !interaction.member) {
    return errorResponse("This command can only be used in a server.");
  }

  const inputColor = getOptionValue<string>(interaction, "color");
  if (inputColor === undefined) {
    return errorResponse("Choose a color from the palette.");
  }

  const selectedColor = COLOR_PALETTE.find(
    (option) => option.value === inputColor,
  );
  if (!selectedColor) {
    return errorResponse("Choose one of the available palette colors.");
  }

  try {
    await setMemberColor(guildId, user.id, selectedColor.value);
  } catch (error) {
    console.error("Failed to update color:", error);
    return errorResponse(
      "I couldn't update your color. The bot needs Manage Roles and must be ranked above your color role.",
    );
  }

  return embedResponse(
    {
      title: "Name Color",
      description: `Your name color is now **${selectedColor.name}**.`,
      color: selectedColor.color,
    },
    true,
  );
}
