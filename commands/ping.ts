import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse } from "../utils/discord";

export async function handlePing(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  // Serverless doesn't maintain a WebSocket connection, so we can't measure latency
  // like the Python bot could. Just respond with pong.
  return embedResponse({
    title: "🏓 Pong!",
    color: Colors.RED,
  });
}
