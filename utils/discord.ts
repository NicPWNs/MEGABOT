import {
  InteractionResponse,
  InteractionResponseType,
  InteractionResponseData,
  DiscordEmbed,
  ActionRow,
  ButtonComponent,
  ButtonStyle,
  MessageFlags,
  Colors,
} from "../types/discord";

/**
 * Create a simple text response
 */
export function textResponse(
  content: string,
  ephemeral = false,
): InteractionResponse {
  return {
    type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    data: {
      content,
      flags: ephemeral ? MessageFlags.EPHEMERAL : undefined,
    },
  };
}

/**
 * Create an embed response
 */
export function embedResponse(
  embed: DiscordEmbed,
  ephemeral = false,
  components?: ActionRow[],
): InteractionResponse {
  return {
    type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    data: {
      embeds: [embed],
      components,
      flags: ephemeral ? MessageFlags.EPHEMERAL : undefined,
    },
  };
}

/**
 * Create an error response (ephemeral)
 */
export function errorResponse(message: string): InteractionResponse {
  return embedResponse(
    {
      title: "❌ Error",
      description: message,
      color: Colors.RED,
    },
    true,
  );
}

/**
 * Create a loading response
 */
export function loadingResponse(message = "Loading..."): InteractionResponse {
  return embedResponse({
    title: `⏳ ${message}`,
    color: Colors.GOLD,
  });
}

/**
 * Create a PONG response for Discord's ping
 */
export function pongResponse(): InteractionResponse {
  return {
    type: InteractionResponseType.PONG,
  };
}

/**
 * Create a deferred response (for longer operations)
 */
export function deferredResponse(ephemeral = false): InteractionResponse {
  return {
    type: InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
    data: {
      flags: ephemeral ? MessageFlags.EPHEMERAL : undefined,
    },
  };
}

/**
 * Create an update message response (for component interactions)
 */
export function updateResponse(
  embed: DiscordEmbed,
  components?: ActionRow[],
): InteractionResponse {
  return {
    type: InteractionResponseType.UPDATE_MESSAGE,
    data: {
      embeds: [embed],
      components,
    },
  };
}

/**
 * Create a button row
 */
export function createButtonRow(
  buttons: {
    customId: string;
    label: string;
    style: ButtonStyle;
    emoji?: string;
    disabled?: boolean;
  }[],
): ActionRow {
  return {
    type: 1,
    components: buttons.map((btn) => ({
      type: 2,
      style: btn.style,
      label: btn.label,
      custom_id: btn.customId,
      emoji: btn.emoji ? { name: btn.emoji } : undefined,
      disabled: btn.disabled,
    })),
  };
}

/**
 * Send a follow-up message to a deferred interaction
 */
export async function sendFollowUp(
  applicationId: string,
  interactionToken: string,
  data: InteractionResponseData,
): Promise<void> {
  const url = `https://discord.com/api/v10/webhooks/${applicationId}/${interactionToken}`;

  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

/**
 * Edit the original response
 */
export async function editOriginalResponse(
  applicationId: string,
  interactionToken: string,
  data: InteractionResponseData,
): Promise<void> {
  const url = `https://discord.com/api/v10/webhooks/${applicationId}/${interactionToken}/messages/@original`;

  await fetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

/**
 * Send a message to a channel
 */
export async function sendChannelMessage(
  channelId: string,
  data: { content?: string; embeds?: DiscordEmbed[] },
): Promise<void> {
  const botToken = process.env.DISCORD_BOT_TOKEN;
  const url = `https://discord.com/api/v10/channels/${channelId}/messages`;

  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bot ${botToken}`,
    },
    body: JSON.stringify(data),
  });
}

/**
 * Get guild members (for boost reward)
 */
export async function getGuildMembers(guildId: string): Promise<any[]> {
  const botToken = process.env.DISCORD_BOT_TOKEN;
  const url = `https://discord.com/api/v10/guilds/${guildId}/members?limit=1000`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bot ${botToken}`,
    },
  });

  return (await response.json()) as any[];
}

/**
 * Get guild premium subscribers (boosters)
 */
export async function getGuildBoosters(guildId: string): Promise<any[]> {
  const members = await getGuildMembers(guildId);
  return members.filter((member: any) => member.premium_since !== null);
}
