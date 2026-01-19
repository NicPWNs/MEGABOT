import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  MEGACOIN_EMOJI,
} from "../types/discord";
import { embedResponse } from "../utils/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import {
  processStreak,
  getStreakStats,
  getStreakData,
} from "../services/streak";
import { addCoins } from "../services/megacoin";

/**
 * Get streak emoji based on streak count (matches Python)
 */
function getStreakEmoji(streak: number): string {
  if (streak < 2) return "💩";
  if (streak < 3) return "✌️";
  if (streak < 4) return "👌";
  if (streak < 5) return "🍀";
  if (streak < 10) return "🔥";
  if (streak < 25) return "🧨";
  if (streak < 50) return "🏆";
  if (streak < 69) return "💀";
  if (streak === 69) return "-  *nice*.";
  if (streak < 75) return "💀";
  if (streak < 100) return "💎";
  if (streak === 100) return "💯 - *Welcome to Party Mode*";
  return "🎉🎊🎉🎊🎉"; // Party mode for 100+
}

/**
 * Calculate streak reward (matches Python logic)
 * Coins = streak count, capped at 100
 * Bonus = streak value at every 100 milestone
 */
function calculateStreakReward(streak: number): {
  coins: number;
  bonus: number;
} {
  const coins = Math.min(streak, 100);
  const bonus = streak % 100 === 0 ? streak : 0;
  return { coins, bonus };
}

export async function handleStreak(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const showStats = getOptionValue<boolean>(interaction, "stats");
  const user = getUser(interaction);

  // If stats requested, show stats
  if (showStats) {
    const stats = await getStreakStats();
    const userData = await getStreakData(user.id);

    return embedResponse({
      title: "📊 Streak Stats",
      description:
        `**Your Stats:**\n` +
        `Current Streak: **${userData?.streak || 0}** days\n` +
        `Personal Record: **${userData?.personalRecord || 0}** days\n\n` +
        `**Server Records:**\n` +
        `🏆 All-Time Record: **${stats.allTimeStreak.stat}** days by <@${stats.allTimeStreak.userId}>\n` +
        `🔥 Current Highest: **${stats.currentStreak.stat}** days by <@${stats.currentStreak.userId}>`,
      color: Colors.GOLD,
    });
  }

  // Process the streak
  const botUserId = interaction.application_id;
  const result = await processStreak(
    user.id,
    user.username,
    botUserId,
    "MEGABOT",
  );

  // Get emoji based on streak
  const streakEmoji = getStreakEmoji(result.streak);

  // Calculate color based on missed status
  const color = result.prefix.includes("missed") ? Colors.RED : Colors.BLUE;

  // Build response
  const title = `${result.prefix}Your streak is: ${result.streak}  ${streakEmoji}`;

  if (result.hit) {
    // Award MEGACOIN based on streak (coins = streak, capped at 100, plus bonus at milestones)
    const { coins, bonus } = calculateStreakReward(result.streak);
    const totalReward = coins + bonus;
    await addCoins(user.id, user.username, totalReward);

    let description = `+ ${coins} ${MEGACOIN_EMOJI}`;
    if (bonus > 0) {
      description += `  + ${bonus} bonus ${MEGACOIN_EMOJI}`;
    }

    return embedResponse({
      title,
      description,
      color,
    });
  } else {
    // Already hit streak today
    return embedResponse({
      title,
      description: "You've already hit your streak today! Come back tomorrow.",
      color: Colors.YELLOW,
    });
  }
}
