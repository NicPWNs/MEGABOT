import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime


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
            'id': str(139927805117857791)
        }
    )

    dataLength = int(data['ResponseMetadata']
                     ['HTTPHeaders']['content-length'])

    # 2023-02-22 21:11:05.800895
    if dataLength > 5:
        storedLastMid = datetime.fromisoformat(data['Item']['lastMid'])
        storedNextMid = datetime.fromisoformat(data['Item']['nextMid'])
        storedSkipMid = datetime.fromisoformat(data['Item']['skipMid'])

    await ctx.edit(content=f"{storedNextMid}")
