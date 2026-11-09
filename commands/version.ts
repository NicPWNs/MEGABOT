import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { Octokit } from "@octokit/rest";

const FALLBACK_VERSION = "v3.1";

export async function handleVersion(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const botId = interaction.application_id;

  try {
    const octokit = new Octokit({
      auth: process.env.GITHUB_TOKEN,
    });

    const { data: releases } = await octokit.repos.listReleases({
      owner: "NicPWNs",
      repo: "MEGABOT",
      per_page: 1,
    });

    const latestRelease = releases[0]?.tag_name || FALLBACK_VERSION;

    return embedResponse({
      title: "📦 Current Version",
      description: `The latest <@${botId}> release is [**${latestRelease}**](https://github.com/NicPWNs/MEGABOT/releases)`,
      color: 0xd89b82,
    });
  } catch (error) {
    console.error("GitHub API error:", error);
    // Fallback to hardcoded version
    return embedResponse({
      title: "📦 Current Version",
      description: `The latest <@${botId}> release is [**${FALLBACK_VERSION}**](https://github.com/NicPWNs/MEGABOT/releases)`,
      color: 0xd89b82,
    });
  }
}
