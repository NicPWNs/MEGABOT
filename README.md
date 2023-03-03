# MEGABOT Discord Bot

![ezgif-4-5ac6df3cf6](https://user-images.githubusercontent.com/23003787/222802520-b4bb79a0-21d7-4f73-a992-f1ff01fd154a.gif)

Another Discord bot for learning and fun. Using ~~discord.py~~ `pycord` to practice CI/CD with GitHub actions and EC2. Not serverless, unfortunately. 😞

## 🤖 Commands

- `/age <name>`: Guesses the age of a specified name.
- `/bless`: Blesses the mess!
- `/chat <prompt>`: Chat with MEGABOT. (GPT3)
- `/csgo <username>`: Retrieve CS:GO stats.
- `/emote <search> [add:true]`: Search for a 7TV emote. Optionally add it to the Discord guild.
- `/kanye`: Retrieve a random Kanye West quote.
- `/kill`: Stop the bot's process.
- `/math <expression>`: Evaluate provided math expression.
- `/nasa [details:True]`: Retrieve the NASA photo of the day.
- `/pause`: Pauses music.
- `/ping`: Responds with pong.
- `/play`: Plays music.
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
- [ ] Improve CI/CD with checks/tests (lint)
