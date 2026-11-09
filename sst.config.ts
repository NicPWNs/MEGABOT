/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "megabot",
      removal: input?.stage === "prod" ? "retain" : "remove",
      protect: ["prod"].includes(input?.stage),
      home: "aws",
      providers: {
        aws: {
          region: "us-east-1",
        },
      },
    };
  },
  async run() {
    // Environment variables (names match `sst secret set` values)
    const discordPublicKey = new sst.Secret("DiscordPublicKey");
    const discordAppId = new sst.Secret("DiscordApplicationId");
    const discordBotToken = new sst.Secret("DiscordToken");
    const githubToken = new sst.Secret("GithubToken");
    const nasaKey = new sst.Secret("NasaApiKey");
    const stockKey = new sst.Secret("StockKey");
    const guildId = new sst.Secret("MegacordGuildId");
    const mainChannelId = new sst.Secret("MainChannelId");
    const adminIds = new sst.Secret("AdminIds");
    const photoBucket = new sst.Secret("PhotoBucket");

    // Use existing DynamoDB tables from Python bot (not managed by SST)
    const megacoinTableName = "discord-megacoin";
    const streakTableName = "discord-streak";
    const photosTableName = "discord-photos";

    // Main Discord Interaction Handler (API Gateway + Lambda)
    const api = new sst.aws.ApiGatewayV2("DiscordApi");

    const interactionHandler = new sst.aws.Function("InteractionHandler", {
      handler: "handlers/interaction.handler",
      timeout: "15 seconds",
      memory: "256 MB",
      environment: {
        DISCORD_PUBLIC_KEY: discordPublicKey.value,
        DISCORD_APPLICATION_ID: discordAppId.value,
        DISCORD_BOT_TOKEN: discordBotToken.value,
        GITHUB_TOKEN: githubToken.value,
        NASA_KEY: nasaKey.value,
        STOCK_KEY: stockKey.value,
        GUILD_ID: guildId.value,
        ADMIN_IDS: adminIds.value,
        MEGACOIN_TABLE: megacoinTableName,
        STREAK_TABLE: streakTableName,
        PHOTOS_TABLE: photosTableName,
        PHOTO_BUCKET: photoBucket.value,
      },
      permissions: [
        {
          actions: [
            "dynamodb:GetItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
            "dynamodb:Scan",
          ],
          resources: [
            `arn:aws:dynamodb:*:*:table/${megacoinTableName}`,
            `arn:aws:dynamodb:*:*:table/${streakTableName}`,
            `arn:aws:dynamodb:*:*:table/${photosTableName}`,
          ],
        },
        {
          actions: ["s3:GetObject", "s3:PutObject"],
          resources: ["arn:aws:s3:::*/*"],
        },
      ],
    });

    api.route("POST /interactions", interactionHandler.arn);

    // Scheduled Jobs

    // Boost Reward - 1st of each month at 1 PM UTC
    new sst.aws.Cron("BoostRewardJob", {
      schedule: "cron(0 13 1 * ? *)",
      job: {
        handler: "handlers/jobs/boost-reward.handler",
        timeout: "30 seconds",
        memory: "256 MB",
        environment: {
          DISCORD_BOT_TOKEN: discordBotToken.value,
          GUILD_ID: guildId.value,
          MAIN_CHANNEL_ID: mainChannelId.value,
          MEGACOIN_TABLE: megacoinTableName,
        },
        permissions: [
          {
            actions: [
              "dynamodb:GetItem",
              "dynamodb:PutItem",
              "dynamodb:UpdateItem",
            ],
            resources: [`arn:aws:dynamodb:*:*:table/${megacoinTableName}`],
          },
        ],
      },
    });

    // Fill missing member colors and assign colors to members who have joined
    // since the previous scan. Existing color roles are left as-is.
    new sst.aws.Cron("MemberColorJob", {
      schedule: "rate(5 minutes)",
      job: {
        handler: "handlers/jobs/member-colors.handler",
        timeout: "15 minutes",
        memory: "1024 MB",
        concurrency: { reserved: 1 },
        environment: {
          DISCORD_BOT_TOKEN: discordBotToken.value,
          GUILD_ID: guildId.value,
        },
      },
    });

    return {
      apiUrl: api.url,
      interactionsEndpoint: $interpolate`${api.url}interactions`,
    };
  },
});
