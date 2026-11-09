import { DiscordInteraction, InteractionResponse } from "../types/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { embedResponse, errorResponse } from "../utils/discord";
import { setMegamodColor } from "../utils/discord-api";

const MEGAMODS_ROLE_ID = "1022557623859556452";

export async function handleMegaColor(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const guildId = interaction.guild_id;
  const user = getUser(interaction);
  if (!guildId || !interaction.member) {
    return errorResponse("This command can only be used in a server.");
  }

  if (!interaction.member.roles.includes(MEGAMODS_ROLE_ID)) {
    return errorResponse("This command is only available to MEGAMODS members.");
  }

  const inputColor = getOptionValue<string>(interaction, "color");
  const reset = getOptionValue<boolean>(interaction, "reset") === true;
  if ((inputColor === undefined) === !reset) {
    return errorResponse("Choose either a hex color or set reset to true.");
  }

  let color: number | null = null;
  if (!reset) {
    const match = inputColor?.match(/^#?([\da-f]{6})$/i);
    if (!match) return errorResponse("Enter a six-digit hex color, such as #ff0000.");
    color = Number.parseInt(match[1], 16);
  }

  try {
    await setMegamodColor(guildId, user.id, color);
  } catch (error) {
    console.error("Failed to update MEGAMODS color:", error);
    return errorResponse(
      "I couldn't update your color. The bot needs Manage Roles, and its role must be above MEGAMODS.",
    );
  }

  return embedResponse(
    {
      title: "MEGAMODS Name Color",
      description: reset
        ? "Your color is back to the default MEGAMODS red."
        : `Your name color is now **#${color!.toString(16).padStart(6, "0").toUpperCase()}**. Use \`/megacolor reset:true\` to return to red.`,
      color: color ?? 0xdd2f45,
    },
    true,
  );
}
