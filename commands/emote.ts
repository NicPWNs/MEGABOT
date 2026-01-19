import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getOptionValue } from "../handlers/commands";

interface SevenTVEmote {
  id: string;
  name: string;
  host: {
    url: string;
    files: { name: string; format: string }[];
  };
}

interface SevenTVSearchResponse {
  emotes: SevenTVEmote[];
}

export async function handleEmote(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const search = getOptionValue<string>(interaction, "search")!;

  try {
    // Search 7TV API
    const url = `https://7tv.io/v3/gql`;
    const query = {
      query: `
        query SearchEmotes($query: String!) {
          emotes(query: $query, limit: 1) {
            items {
              id
              name
              host {
                url
                files {
                  name
                  format
                }
              }
            }
          }
        }
      `,
      variables: { query: search },
    };

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(query),
    });

    const data = (await response.json()) as {
      data: { emotes: { items: SevenTVEmote[] } };
    };
    const emotes = data.data?.emotes?.items;

    if (!emotes || emotes.length === 0) {
      return errorResponse(`No emotes found for "${search}".`);
    }

    const emote = emotes[0];

    // Get the best quality file (prefer WEBP or GIF)
    const webpFile = emote.host.files.find((f) => f.format === "WEBP");
    const gifFile = emote.host.files.find((f) => f.format === "GIF");
    const file = webpFile || gifFile || emote.host.files[0];

    const emoteUrl = `https:${emote.host.url}/${file?.name || "4x.webp"}`;

    return embedResponse({
      title: "🎭 7TV Emote Search",
      description: `Found emote: **${emote.name}**`,
      color: Colors.PURPLE,
      thumbnail: { url: emoteUrl },
    });
  } catch (error) {
    console.error("7TV API error:", error);
    return errorResponse(
      "Failed to search for emotes. Please try again later.",
    );
  }
}
