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

    test1 = f"⚙️ MEGABOT is running on {hostname} (PID {pid})\n\n"
    test2 = f"🐍 MEGABOT is running on Python v{py}\n\n"
    test3 = f"⏲️ MEGABOT has been running for {runTime}s\n\n"
    test4 = f"👂 MEGABOT is testing its event listeners:\n‏"

    content = test1 + test2 + test3 + test4

    await ctx.respond(content=content)
