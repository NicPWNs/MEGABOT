#!/usr/bin/env python3
import os
import sys
import time
import datetime
import platform


async def test(ctx, startTime):

    hostname = platform.node()
    pid = os.getpid()
    py = sys.version[0:3]
    runTime = str(datetime.timedelta(seconds=int(time.time() - startTime)))

    if "ec2" in hostname:
        hostname = "AWS"

    content = f"āļø MEGABOT is running on **{hostname}** (PID {pid})\n\n"
    content += f"š MEGABOT is running on **Python v{py}**\n\n"
    content += f"ā²ļø MEGABOT is running for **{runTime}s**\n\n"
    content += f"š MEGABOT is testing event listeners:\nā"

    await ctx.respond(content=content)

    await ctx.channel.send('ā Testing event listeners...')
