/**
 * Discord REST API utilities for making authenticated API calls
 */

import { COLOR_PALETTE } from "../types/commands";

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

  let response: Response;
  for (let attempt = 0; ; attempt++) {
    response = await fetch(`${DISCORD_API}${endpoint}`, {
      method: options.method || "GET",
      headers: {
        Authorization: `Bot ${token}`,
        "Content-Type": "application/json",
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
    });
    if (response.status !== 429 || attempt >= 5) break;
    const rateLimit = (await response.json()) as { retry_after?: number };
    const retryAfterMs = Math.ceil((rateLimit.retry_after ?? 1) * 1000);
    await new Promise((resolve) => setTimeout(resolve, retryAfterMs));
  }

  if (!response.ok) {
    const error = await response.text();
    console.error(`Discord API error: ${response.status} - ${error}`);
    throw new Error(`Discord API error: ${response.status}`);
  }

  // Several Discord endpoints (including adding/removing member roles) return
  // 204 No Content, so there is no JSON body to parse.
  if (response.status === 204) return undefined as T;

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

const SHARED_COLOR_ROLE_PREFIX = "MEGABOT-COLOR-";
const LEGACY_COLOR_ROLE_PREFIX = "MEGAMOD-COLOR-";

export interface GuildRole {
  id: string;
  name: string;
  color: number;
  position: number;
}

export interface GuildMemberResponse {
  user: DiscordGuildUser;
  nick?: string;
  roles: string[];
  joined_at?: string;
  premium_since?: string;
}

export interface DiscordGuildUser {
  id: string;
  username: string;
  bot?: boolean;
}

export interface ColorRoleState {
  roles: GuildRole[];
  byValue: Map<string, GuildRole>;
  roleIds: Set<string>;
}

/** Ensure shared palette roles exist at the bottom of the guild role list. */
export async function ensureColorRoles(
  guildId: string,
): Promise<ColorRoleState> {
  const roles = await discordFetch<GuildRole[]>(`/guilds/${guildId}/roles`);

  for (const color of COLOR_PALETTE) {
    const roleName = `${SHARED_COLOR_ROLE_PREFIX}${color.value.toUpperCase()}`;
    let role = roles.find((existing) => existing.name === roleName);
    if (!role) {
      role = await discordFetch<GuildRole>(`/guilds/${guildId}/roles`, {
        method: "POST",
        body: {
          name: roleName,
          color: color.color,
          permissions: "0",
          hoist: false,
          mentionable: false,
        },
      });
      roles.push(role);
    }
  }

  let colorRoles = COLOR_PALETTE.flatMap((color) => {
    const role = roles.find(
      (existing) =>
        existing.name ===
        `${SHARED_COLOR_ROLE_PREFIX}${color.value.toUpperCase()}`,
    );
    return role ? [role] : [];
  });
  const bottomOrder = [...colorRoles].sort((a, b) => a.position - b.position);
  if (bottomOrder.some((role, index) => role.position !== index + 1)) {
    let currentRoles = roles;
    for (const colorRole of bottomOrder) {
      const currentRole = currentRoles.find((role) => role.id === colorRole.id);
      if (!currentRole || currentRole.position === 1) continue;
      await discordFetch<GuildRole[]>(`/guilds/${guildId}/roles`, {
        method: "PATCH",
        body: [{ id: currentRole.id, position: 1 }],
      });
      currentRoles = await discordFetch<GuildRole[]>(
        `/guilds/${guildId}/roles`,
      );
    }
    colorRoles = COLOR_PALETTE.flatMap((color) => {
      const name = `${SHARED_COLOR_ROLE_PREFIX}${color.value.toUpperCase()}`;
      const role = currentRoles.find((existing) => existing.name === name);
      return role ? [role] : [];
    });
  }

  const roleIds = new Set(colorRoles.map((role) => role.id));
  const byValue = new Map(
    COLOR_PALETTE.flatMap((color) => {
      const role = colorRoles.find(
        (existing) =>
          existing.name ===
          `${SHARED_COLOR_ROLE_PREFIX}${color.value.toUpperCase()}`,
      );
      return role ? [[color.value, role] as const] : [];
    }),
  );

  return {
    roles: [...roles.filter((role) => !roleIds.has(role.id)), ...colorRoles],
    byValue,
    roleIds,
  };
}

/** Assign a shared palette role, removing any previous shared or legacy color role. */
export async function assignColorRole(
  guildId: string,
  userId: string,
  roleId: string,
  memberRoles: string[],
  roleState: ColorRoleState,
): Promise<void> {
  const legacyRole = roleState.roles.find(
    (role) => role.name === `${LEGACY_COLOR_ROLE_PREFIX}${userId}`,
  );
  const oldRoleIds = memberRoles.filter(
    (id) => roleState.roleIds.has(id) || id === legacyRole?.id,
  );
  if (oldRoleIds.length) {
    for (const oldRoleId of oldRoleIds) {
      await discordFetch(
        `/guilds/${guildId}/members/${userId}/roles/${oldRoleId}`,
        { method: "DELETE" },
      );
    }
  }
  await discordFetch(
    `/guilds/${guildId}/members/${userId}/roles/${roleId}`,
    { method: "PUT" },
  );
}

export async function setMegamodColor(
  guildId: string,
  userId: string,
  colorValue: string,
): Promise<void> {
  const roleState = await ensureColorRoles(guildId);
  const role = roleState.byValue.get(colorValue);
  if (!role) throw new Error("Unknown palette color");
  const member = await getGuildMember(guildId, userId);
  if (!member) throw new Error("Guild member was not found");
  await assignColorRole(guildId, userId, role.id, member.roles, roleState);
}

export async function getGuildMembersPage(
  guildId: string,
  after?: string,
): Promise<GuildMemberResponse[]> {
  const query = new URLSearchParams({ limit: "1000" });
  if (after) query.set("after", after);
  return discordFetch<GuildMemberResponse[]>(
    `/guilds/${guildId}/members?${query.toString()}`,
  );
}

export function isColorRole(role: GuildRole): boolean {
  return (
    role.name.startsWith(SHARED_COLOR_ROLE_PREFIX) ||
    role.name.startsWith(LEGACY_COLOR_ROLE_PREFIX)
  );
}

// Type definitions
