import os
import boto3


async def streak(ctx, stats):

    await ctx.respond(content="*⏳ Loading...*")

    content = "Good!"

    await ctx.edit(content=f"{content}")
