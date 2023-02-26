#!/usr/bin/env python3
import os
import sys
import time
import platform


async def test(ctx, startTime):

    hostname = platform.node()
    pid = os.getpid()
    py = sys.version[0:3]
    runTime = int(time.time() - startTime)

    test1 = f"⚙️ MEGABOT is running on {hostname} (PID {pid})\n\n"
    test2 = f"🐍 MEGABOT is running on Python version {py}\n\n"
    test3 = f"⏲️ MEGABOT has been running for {runTime}s\n\n"
    test4 = f"👂 MEGABOT is testing its event listeners:"

    content = test1 + test2 + test3 + test4

    await ctx.respond(content=content)
