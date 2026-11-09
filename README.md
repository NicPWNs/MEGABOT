# MEGABOT Discord Bot (Serverless)

![MEGACORD LOGO](/images/thumbnail.gif)

MEGABOT is a customized Discord bot written in **TypeScript** and deployed on AWS Lambda using [SST](https://sst.dev).

> Originally based on [BlessThisMess](https://github.com/NicPWNs/Discord-BTM-Bot).

## Commands

- `/balance [user]`: View a MEGACOIN balance.
- `/bank`: View the MEGACOIN leaderboard.
- `/blackjack <wager>`: Play MEGACOIN blackjack.
- `/bless`: Blesses the mess!
- `/bug <title> <description>`: Report a MEGABOT bug.
- `/coin`: Flip a coin.
- `/color`: Set or reset your name color (available to all members).
- `/dice`: Roll a dice.
- `/double <wager>`: Play MEGACOIN double or nothing.
- `/emote <search>`: Search for a 7TV emote.
- `/feature <title> <description>`: Submit a feature request.
- `/kanye`: Retrieve a random Kanye West quote.
- `/math <expression>`: Evaluate a math expression.
- `/mc`: View the Minecraft Speed Running Leaderboard.
- `/nasa [details]`: Retrieve NASA's photo of the day.
- `/pay <user> <amount>`: Pay another user MEGACOIN.
- `/payout <user> <amount> <message>`: Pay out MEGACOIN (requires the MEGALORDS role).
- `/photo`: Return a random photo from the MEGABOT database.
- `/ping`: Respond with pong.
- `/poll`: Create a Discord poll with up to nine options.
- `/streak [stats]`: Keep a daily streak going or view streak stats.
- `/stock <symbol>`: Search for a stock price.
- `/version`: View the latest MEGABOT release.
- `/weather <zipcode>`: Get a seven-day weather forecast.
- `/wheel <wager>`: Spin the MEGACOIN wheel.

The bot needs Manage Roles, its highest role must be above the color roles it creates, and those color roles must be above MEGAMODS to override that role's color. Music, AI chat/image, and persistent event commands are not supported in the serverless version.

## Release announcements

When a stable GitHub release is published, MEGABOT posts an announcement in the configured Discord channel. Add a `## Discord Announcement` section to the release notes with one concise item per line; the workflow posts those items as bullets beneath a bold release heading. The GitHub release webhook posts its own notification separately.
