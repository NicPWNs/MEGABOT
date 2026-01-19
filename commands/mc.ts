import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getUser } from "../handlers/commands";

interface MCSRRankedResponse {
  status: "success" | "error";
  data?: {
    nickname: string;
    statistics: {
      total: {
        bestTime: {
          ranked: number | null;
          casual: number | null;
        };
      };
    };
  };
}

export async function handleMc(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const user = getUser(interaction);

  try {
    // Check if the user has an mcsrranked account linked to their Discord
    const response = await fetch(
      `https://mcsrranked.com/api/users/discord.${user.id}`,
    );
    const data = (await response.json()) as MCSRRankedResponse;

    if (data.status === "error") {
      return embedResponse({
        title: "<:MCSR:1372588978959548527> Minecraft Speed Running",
        description:
          "You don't have an MCSR Ranked account linked to your Discord!\n\n" +
          "Link your account at [mcsrranked.com](https://mcsrranked.com/) to see your stats.",
        color: Colors.YELLOW,
      });
    }

    const ranked = data.data?.statistics.total.bestTime.ranked ?? null;
    const casual = data.data?.statistics.total.bestTime.casual ?? null;
    const nickname = data.data?.nickname || "Unknown";

    // Get best time between ranked and casual
    let bestTime: number | null = null;
    if (ranked !== null && casual !== null) {
      bestTime = Math.min(ranked, casual);
    } else if (ranked !== null) {
      bestTime = ranked;
    } else if (casual !== null) {
      bestTime = casual;
    }

    if (bestTime === null) {
      return embedResponse({
        title: "<:MCSR:1372588978959548527> Minecraft Speed Running",
        description: `**${nickname}** hasn't completed any speedruns yet!\n\nStart running at [mcsrranked.com](https://mcsrranked.com/)`,
        color: Colors.YELLOW,
      });
    }

    // Convert milliseconds to minutes:seconds
    const minutes = Math.floor(bestTime / 60000);
    const seconds = Math.floor((bestTime % 60000) / 1000);
    const timeStr = `${minutes}:${seconds.toString().padStart(2, "0")}`;

    return embedResponse({
      title: "<:MCSR:1372588978959548527> Minecraft Speed Running",
      description:
        `**${nickname}**'s Best Time: **${timeStr}**\n\n` +
        `View full stats at [mcsrranked.com](https://mcsrranked.com/profile/${nickname})`,
      color: Colors.GREEN,
    });
  } catch (error) {
    console.error("MCSR Ranked API error:", error);
    return errorResponse("Failed to fetch Minecraft speedrun data.");
  }
}
