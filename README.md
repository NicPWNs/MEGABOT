# MEGABOT Discord Bot

![](/thumbnail.gif)

Another Discord bot for learning and fun. Using ~~discord.py~~ `pycord` to practice CI/CD with GitHub actions and EC2. Not serverless, unfortunately. 😞

> Some commands use my own Python package: [random-unicode-emoji](https://github.com/NicPWNs/random_unicode_emoji)

## 🤖 Commands

- `/age <name>`: Guesses the age of a specified name.
- `/bless`: Blesses the mess!
- `/chat <prompt>`: Chat with MEGABOT. (GPT3.5)
- `/coin`: Flip a coin.
- `/csgo <username>`: Retrieve CS:GO stats.
- `/dice`: Roll a dice.
- `/emote <search> [add:true]`: Search for a 7TV emote. Optionally add it to the Discord guild.
- `/image`: Generate an image with AI.
- `/kanye`: Retrieve a random Kanye West quote.
- `/kill`: Stop the bot's process.
- `/math <expression>`: Evaluate provided math expression.
- `/nasa [details:True]`: Retrieve the NASA photo of the day.
- `/pause`: Pauses music.
- `/ping`: Responds with pong.
- `/play`: Plays music.
- `/randomemoji`: Return a random emoji.
- `/resume`: Resumes music.
- `/stop`: Stops music.
- `/stock`: Searches a stock price.
- `/streak [stats:True]`: Keep a daily streak going!
- `/test`: Run a series of tests on the bot.

## 💡 To-Do

- [x] Add `/` application commands
- [x] Migrate all working commands from [BlessThisMess](https://github.com/NicPWNs/Discord-BTM-Bot)
- [x] Add `/emote`. Was broken on [BlessThisMess](https://github.com/NicPWNs/Discord-BTM-Bot)
- [x] Restructure project and commands
- [x] Add random emoji to `/streak` > 100
- [x] Fix DST for `/streak`
- [x] Add `/play`. Music!
- [ ] Add `/queue` and `/skip` to music
- [ ] Add logging
- [ ] Improve CI/CD with checks/tests (lint)
