import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import {
  DiscordInteraction,
  InteractionType,
  InteractionResponse,
} from "../types/discord";
import { verifyDiscordSignature } from "../utils/verify";
import { pongResponse } from "../utils/discord";
import { handleSlashCommand } from "./commands";
import { handleComponentInteraction } from "./components";

/**
 * Main Lambda handler for Discord interactions
 */
export async function handler(
  event: APIGatewayProxyEvent,
): Promise<APIGatewayProxyResult> {
  // Log for debugging
  console.log("Received interaction:", JSON.stringify(event, null, 2));

  // Verify the request signature
  const signature = event.headers["x-signature-ed25519"];
  const timestamp = event.headers["x-signature-timestamp"];
  const publicKey = process.env.DISCORD_PUBLIC_KEY;

  if (!signature || !timestamp || !publicKey || !event.body) {
    return {
      statusCode: 401,
      body: JSON.stringify({ error: "Invalid request signature" }),
    };
  }

  const isValidRequest = verifyDiscordSignature(
    publicKey,
    signature,
    timestamp,
    event.body,
  );

  if (!isValidRequest) {
    return {
      statusCode: 401,
      body: JSON.stringify({ error: "Invalid request signature" }),
    };
  }

  // Parse the interaction
  const interaction: DiscordInteraction = JSON.parse(event.body);

  // Handle different interaction types
  let response: InteractionResponse;

  try {
    switch (interaction.type) {
      case InteractionType.PING:
        // Respond to Discord's ping (used for webhook URL validation)
        response = pongResponse();
        break;

      case InteractionType.APPLICATION_COMMAND:
        // Handle slash commands
        response = await handleSlashCommand(interaction);
        break;

      case InteractionType.MESSAGE_COMPONENT:
        // Handle button clicks and select menus
        response = await handleComponentInteraction(interaction);
        break;

      default:
        console.warn("Unknown interaction type:", interaction.type);
        response = {
          type: 4,
          data: {
            content: "Unknown interaction type",
            flags: 64,
          },
        };
    }
  } catch (error) {
    console.error("Error handling interaction:", error);
    response = {
      type: 4,
      data: {
        content: "❌ An error occurred while processing your request.",
        flags: 64,
      },
    };
  }

  const result = {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(response),
  };

  console.log("Returning response:", JSON.stringify(result, null, 2));
  return result;
}
