import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { Octokit } from "@octokit/rest";

export async function handleBug(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const title = getOptionValue<string>(interaction, "title")!;
  const description = getOptionValue<string>(interaction, "description")!;
  const user = getUser(interaction);

  const githubToken = process.env.GITHUB_TOKEN;
  if (!githubToken) {
    return errorResponse("GitHub integration not configured.");
  }

  try {
    const octokit = new Octokit({ auth: githubToken });

    const body = `${description}\n\n> Submitted by \`${user.username}\``;

    const { data: issue } = await octokit.issues.create({
      owner: "NicPWNs",
      repo: "MEGABOT",
      title,
      body,
      labels: ["bug"],
      assignees: ["NicPWNs"],
    });

    return embedResponse({
      title: `🪲 Created New Bug #${issue.number}`,
      description: `[${issue.title}](${issue.html_url})`,
      color: Colors.GREEN,
    });
  } catch (error) {
    console.error("GitHub API error:", error);
    return errorResponse(
      "Failed to create bug report. Please try again later.",
    );
  }
}
