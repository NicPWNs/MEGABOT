import boto3
from boto3.dynamodb.conditions import Key


async def streak(ctx, stats):

    await ctx.respond(content="*⏳ Loading...*")

    TABLE = "discord-streak"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    dataStats = table.get_item(
        Key={
            'id': 'allTimeStreak'
        }
    )

    dataCurrent = table.get_item(
        Key={
            'id': 'currentStreak'
        }
    )

    data = table.get_item(
        Key={
            'id': ctx.user.id
        }
    )

    content = data["Items"]["streak"]
    await ctx.edit(content=f"{content}")
