/**
 * Script to register Discord slash commands
 * Run with: npm run register-commands
 * Or directly: sst shell -- npx tsx scripts/register-commands.ts
 */

import { COMMANDS } from "../types/commands.js";

// SST shell injects secrets as SCREAMING_SNAKE_CASE env vars
const DISCORD_APPLICATION_ID = process.env.DISCORD_APPLICATION_ID;
const DISCORD_BOT_TOKEN = process.env.DISCORD_TOKEN;
const GUILD_ID = process.env.MEGACORD_GUILD_ID; // Optional: for guild-specific commands

async function registerCommands() {
  if (!DISCORD_APPLICATION_ID || !DISCORD_BOT_TOKEN) {
    console.error(
      "Missing DISCORD_APPLICATION_ID or DISCORD_BOT_TOKEN environment variables",
    );
    process.exit(1);
  }

  // Use guild endpoint for faster updates during development
  // Use global endpoint for production
  const url = GUILD_ID
    ? `https://discord.com/api/v10/applications/${DISCORD_APPLICATION_ID}/guilds/${GUILD_ID}/commands`
    : `https://discord.com/api/v10/applications/${DISCORD_APPLICATION_ID}/commands`;

  console.log(`Registering ${COMMANDS.length} commands...`);
  console.log(`Endpoint: ${GUILD_ID ? "Guild-specific" : "Global"}`);

  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bot ${DISCORD_BOT_TOKEN}`,
      },
      body: JSON.stringify(COMMANDS),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error("Failed to register commands:", error);
      process.exit(1);
    }

    const data = (await response.json()) as Array<{ name: string }>;
    console.log(`Successfully registered ${data.length} commands:`);
    data.forEach((cmd) => {
      console.log(`  - /${cmd.name}`);
    });
  } catch (error) {
    console.error("Error registering commands:", error);
    process.exit(1);
  }
}

registerCommands();
