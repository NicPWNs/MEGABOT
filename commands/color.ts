import { DiscordInteraction, InteractionResponse } from "../types/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { embedResponse, errorResponse } from "../utils/discord";
import { setMegamodColor } from "../utils/discord-api";

const MODERATOR_ROLE_ID = "1022557623859556452";

const NAMED_COLORS: Record<string, number> = {
  black: 0x000000,
  white: 0xffffff,
  gray: 0x808080,
  grey: 0x808080,
  silver: 0xc0c0c0,
  red: 0xff0000,
  darkred: 0x8b0000,
  crimson: 0xdc143c,
  coral: 0xff7f50,
  tomato: 0xff6347,
  salmon: 0xfa8072,
  pink: 0xffc0cb,
  deeppink: 0xff1493,
  hotpink: 0xff69b4,
  orange: 0xffa500,
  darkorange: 0xff8c00,
  gold: 0xffd700,
  yellow: 0xffff00,
  khaki: 0xf0e68c,
  olive: 0x808000,
  lime: 0x00ff00,
  chartreuse: 0x7fff00,
  green: 0x008000,
  forestgreen: 0x228b22,
  seagreen: 0x2e8b57,
  teal: 0x008080,
  turquoise: 0x40e0d0,
  cyan: 0x00ffff,
  aqua: 0x00ffff,
  skyblue: 0x87ceeb,
  deepskyblue: 0x00bfff,
  dodgerblue: 0x1e90ff,
  blue: 0x0000ff,
  navy: 0x000080,
  indigo: 0x4b0082,
  purple: 0x800080,
  blueviolet: 0x8a2be2,
  violet: 0xee82ee,
  lavender: 0xe6e6fa,
  magenta: 0xff00ff,
  fuchsia: 0xff00ff,
  brown: 0xa52a2a,
  chocolate: 0xd2691e,
  tan: 0xd2b48c,
  beige: 0xf5f5dc,
  maroon: 0x800000,
  mint: 0x98ff98,
  peach: 0xffdab9,
  plum: 0xdda0dd,
  orchid: 0xda70d6,
};

function parseColor(input: string): number | null {
  const value = input.trim().toLowerCase();
  const hexMatch = value.match(/^#?([\da-f]{6})$/i);
  if (hexMatch) return Number.parseInt(hexMatch[1], 16);
  return NAMED_COLORS[value] ?? null;
}

export async function handleColor(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const guildId = interaction.guild_id;
  const user = getUser(interaction);
  if (!guildId || !interaction.member) {
    return errorResponse("This command can only be used in a server.");
  }

  if (!interaction.member.roles.includes(MODERATOR_ROLE_ID)) {
    return errorResponse("This command is only available to moderators.");
  }

  const inputColor = getOptionValue<string>(interaction, "color");
  const reset = getOptionValue<boolean>(interaction, "reset") === true;
  if ((inputColor === undefined) === !reset) {
    return errorResponse("Choose either a hex color or set reset to true.");
  }

  let color: number | null = null;
  if (!reset) {
    color = inputColor ? parseColor(inputColor) : null;
    if (color === null) {
      return errorResponse(
        "Use a six-digit hex value (with or without #) or a named color such as red, coral, gold, teal, or violet.",
      );
    }
  }

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
        : `Your name color is now **#${color!.toString(16).padStart(6, "0").toUpperCase()}**. Use \`/color reset:true\` to return to red.`,
      color: color ?? 0xdd2f45,
    },
    true,
  );
}
