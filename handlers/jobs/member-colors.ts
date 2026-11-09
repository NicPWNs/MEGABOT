import { ScheduledEvent, Context } from "aws-lambda";
import { COLOR_PALETTE } from "../../types/commands";
import {
  assignColorRole,
  ensureColorRoles,
  GuildMemberResponse,
  getGuildMembersPage,
  isColorRole,
} from "../../utils/discord-api";

const GUILD_ID = process.env.GUILD_ID || "";

/**
 * Periodically assign a random palette color to human members without one.
 * Existing manually selected colors are preserved. The scan also backfills
 * existing members the first time it runs.
 */
export async function handler(
  _event: ScheduledEvent,
  context: Context,
): Promise<void> {
  if (!GUILD_ID) throw new Error("GUILD_ID is not configured");
  console.log("Starting member color scan", { requestId: context.awsRequestId });

  const members: GuildMemberResponse[] = [];
  let after: string | undefined;
  do {
    const page = await getGuildMembersPage(GUILD_ID, after);
    members.push(...page);
    after = page.length === 1000 ? page[page.length - 1].user.id : undefined;
  } while (after);

  const roles = await ensureColorRoles(GUILD_ID, []);
  const roleById = new Map(roles.roles.map((role) => [role.id, role]));
  const uncolored = members.filter(
    (member) =>
      !member.user.bot &&
      !member.roles.some((roleId) => {
        const role = roleById.get(roleId);
        return role ? isColorRole(role) : false;
      }),
  );

  if (uncolored.length === 0) {
    console.log("Member color scan complete; no assignments needed.", {
      members: members.length,
    });
    return;
  }

  const assignments = uncolored.map((member) => ({
    member,
    color: COLOR_PALETTE[Math.floor(Math.random() * COLOR_PALETTE.length)],
  }));
  const roleState = await ensureColorRoles(
    GUILD_ID,
    [...new Set(assignments.map(({ color }) => color.value))],
  );

  let assigned = 0;
  for (const { member, color } of assignments) {
    if (context.getRemainingTimeInMillis() < 20_000) {
      console.warn("Stopping member color scan before Lambda timeout", {
        assigned,
        remaining: assignments.length - assigned,
      });
      break;
    }
    const role = roleState.byValue.get(color.value);
    if (!role) throw new Error(`Missing shared color role for ${color.value}`);
    try {
      await assignColorRole(
        GUILD_ID,
        member.user.id,
        role.id,
        member.roles,
        roleState,
      );
      assigned++;
    } catch (error) {
      console.error(`Could not assign a color to ${member.user.id}:`, error);
    }
  }

  console.log("Member color scan complete.", {
    members: members.length,
    uncolored: uncolored.length,
    assigned,
  });
}
