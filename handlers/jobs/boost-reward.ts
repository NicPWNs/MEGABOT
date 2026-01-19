import { ScheduledEvent, Context } from "aws-lambda";
import { getGuildBoosters, sendChannelMessage } from "../../utils/discord";
import { addCoins } from "../../services/megacoin";
import { Colors, MEGACOIN_EMOJI } from "../../types/discord";

const BOOST_REWARD = 250;
const GUILD_ID = process.env.GUILD_ID || "";
const MAIN_CHANNEL_ID = process.env.MAIN_CHANNEL_ID || "";

/**
 * Monthly boost reward job
 * Runs on the 1st of each month at 1 PM UTC
 */
export async function handler(
  event: ScheduledEvent,
  context: Context,
): Promise<void> {
  console.log("Running boost reward job:", JSON.stringify(event));

  // Check if it's the 1st of the month
  const now = new Date();
  if (now.getUTCDate() !== 1) {
    console.log("Not the 1st of the month, skipping.");
    return;
  }

  try {
    // Get all boosters
    const boosters = await getGuildBoosters(GUILD_ID);

    if (boosters.length === 0) {
      console.log("No boosters found.");
      return;
    }

    console.log(`Found ${boosters.length} boosters.`);

    // Reward each booster
    for (const booster of boosters) {
      const userId = booster.user.id;
      const username = booster.user.username;

      // Add coins
      await addCoins(userId, username, BOOST_REWARD);

      // Send thank you message
      if (MAIN_CHANNEL_ID) {
        await sendChannelMessage(MAIN_CHANNEL_ID, {
          content: `<:boost:1090737525607379025> Thank you for boosting the MEGACORD this month <@${userId}>! + ${BOOST_REWARD} ${MEGACOIN_EMOJI}`,
        });
      }

      console.log(
        `Rewarded ${username} (${userId}) with ${BOOST_REWARD} MEGACOIN.`,
      );
    }

    console.log("Boost reward job completed successfully.");
  } catch (error) {
    console.error("Error in boost reward job:", error);
    throw error;
  }
}
