/**
 * Discord REST API utilities for making authenticated API calls
 */

const DISCORD_API = "https://discord.com/api/v10";

interface DiscordAPIOptions {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
}

/**
 * Make an authenticated Discord API request
 */
async function discordFetch<T>(
  endpoint: string,
  options: DiscordAPIOptions = {},
): Promise<T> {
  const token = process.env.DISCORD_BOT_TOKEN;
  if (!token) {
    throw new Error("DISCORD_BOT_TOKEN not configured");
  }

  const response = await fetch(`${DISCORD_API}${endpoint}`, {
    method: options.method || "GET",
    headers: {
      Authorization: `Bot ${token}`,
      "Content-Type": "application/json",
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const error = await response.text();
    console.error(`Discord API error: ${response.status} - ${error}`);
    throw new Error(`Discord API error: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

/**
 * Create a DM channel with a user and return the channel ID
 */
export async function createDMChannel(userId: string): Promise<string> {
  const data = await discordFetch<{ id: string }>("/users/@me/channels", {
    method: "POST",
    body: { recipient_id: userId },
  });
  return data.id;
}

/**
 * Send a message to a channel
 */
export async function sendMessage(
  channelId: string,
  content: string,
): Promise<void> {
  await discordFetch(`/channels/${channelId}/messages`, {
    method: "POST",
    body: { content },
  });
}

/**
 * Send a DM to a user
 */
export async function sendDM(userId: string, content: string): Promise<void> {
  try {
    const channelId = await createDMChannel(userId);
    await sendMessage(channelId, content);
  } catch (error) {
    console.error(`Failed to send DM to ${userId}:`, error);
    // Don't throw - DM failures shouldn't break the command
  }
}

/**
 * Get a guild member's info including roles
 */
export async function getGuildMember(
  guildId: string,
  userId: string,
): Promise<GuildMemberResponse | null> {
  try {
    return await discordFetch<GuildMemberResponse>(
      `/guilds/${guildId}/members/${userId}`,
    );
  } catch (error) {
    console.error(`Failed to get guild member ${userId}:`, error);
    return null;
  }
}

/**
 * Check if a user has a specific role
 */
export async function userHasRole(
  guildId: string,
  userId: string,
  roleId: string,
): Promise<boolean> {
  const member = await getGuildMember(guildId, userId);
  if (!member) return false;
  return member.roles.includes(roleId);
}

/**
 * Get a role by name in a guild
 */
export async function getRoleByName(
  guildId: string,
  roleName: string,
): Promise<string | null> {
  try {
    const roles = await discordFetch<GuildRole[]>(`/guilds/${guildId}/roles`);
    const role = roles.find(
      (r) => r.name.toLowerCase() === roleName.toLowerCase(),
    );
    return role?.id || null;
  } catch (error) {
    console.error(`Failed to get roles for guild ${guildId}:`, error);
    return null;
  }
}

/**
 * Check if a user has a role by name
 */
export async function userHasRoleByName(
  guildId: string,
  userId: string,
  roleName: string,
): Promise<boolean> {
  const roleId = await getRoleByName(guildId, roleName);
  if (!roleId) return false;
  return userHasRole(guildId, userId, roleId);
}

// Type definitions
interface GuildMemberResponse {
  user?: {
    id: string;
    username: string;
    avatar?: string;
  };
  nick?: string;
  roles: string[];
  premium_since?: string;
}

interface GuildRole {
  id: string;
  name: string;
  color: number;
  position: number;
}
