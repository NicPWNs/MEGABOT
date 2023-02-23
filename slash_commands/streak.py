import boto3
from boto3.dynamodb.conditions import Key


async def streak(ctx, stats):

    await ctx.respond(content="*⏳ Loading...*")

    TABLE = "discord-streak"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    response = table.get_item(
        Key={
            'id': 'allTimeStreak'
        }
    )

    content = response['Item']

    await ctx.edit(content=f"{content}")
