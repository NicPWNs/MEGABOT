#!/usr/bin/env python3
import os
import sys
import time
import datetime
import platform


async def test(ctx, startTime):

    hostname = platform.node()

    if "ec2" in hostname:
        hostname = "AWS"

    content = f"⚙️ <@{ctx.bot.user.id}> is running on **{hostname}** (PID {os.getpid()})\n\n"
    content += f"🐍 <@{ctx.bot.user.id}> is running on **Python v{sys.version[0:3]}**\n\n"
    content += f"⏲️ <@{ctx.bot.user.id}> is running for **{str(datetime.timedelta(seconds=int(time.time() - startTime)))}s**\n\n"
    content += f"👂 <@{ctx.bot.user.id}> is testing event listeners:\n‏"

    await ctx.respond(content=content)
    await ctx.channel.send('⌛ Testing event listeners...')
