#!/usr/bin/env python3
import os
import sys


async def kill(ctx):

    if ctx.user.id == str(os.getenv('OWNER_ID')):
        pid = os.getpid()

        content = f"🛑 **Stopping MEGABOT on PID {pid} !**"
        await ctx.respond(content=content)

        sys.exit()
    else:
        content = f"👅 Nice try! <@{ctx.user.id}> **Permission Denied** ❌"
        await ctx.respond(content=content)
