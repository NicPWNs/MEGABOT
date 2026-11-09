import { DiscordInteraction, InteractionResponse } from "../types/discord";
import { COLOR_PALETTE } from "../types/commands";
import { getOptionValue, getUser } from "../handlers/commands";
import { embedResponse, errorResponse } from "../utils/discord";
import { setMegamodColor } from "../utils/discord-api";

export async function handleColor(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const guildId = interaction.guild_id;
  const user = getUser(interaction);
  if (!guildId || !interaction.member) {
    return errorResponse("This command can only be used in a server.");
  }

  const inputColor = getOptionValue<string>(interaction, "color");
  const reset = getOptionValue<boolean>(interaction, "reset") === true;
  if ((inputColor === undefined) === !reset) {
    return errorResponse("Choose a palette color or set reset to true.");
  }

  const selectedColor = COLOR_PALETTE.find(
    (option) => option.value === inputColor,
  );
  if (!reset && !selectedColor) {
    return errorResponse("Choose one of the available palette colors.");
  }
  const color = reset ? null : selectedColor!.color;

  try {
    await setMegamodColor(guildId, user.id, color);
  } catch (error) {
    console.error("Failed to update color:", error);
    return errorResponse(
      "I couldn't update your color. The bot needs Manage Roles and must be ranked above your color role.",
    );
  }

  return embedResponse(
    {
      title: "Name Color",
      description: reset
        ? "Your color is back to the default color."
        : `Your name color is now **${selectedColor!.name}**. Use \`/color reset:true\` to return to your default color.`,
      color: color ?? 0xdd2f45,
    },
    true,
  );
}
