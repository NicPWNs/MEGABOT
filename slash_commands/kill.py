#!/usr/bin/env python3
import os
import sys


async def kill(ctx):

    pid = os.getpid()

    content = f"🛑 **Stopping MEGABOT on PID {pid} !**"

    await ctx.respond(content=content)

    sys.exit()
