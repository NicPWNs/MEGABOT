#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta
from random_unicode_emoji import random_emoji


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
            'id': str(ctx.user.id)
        }
    )

    dataLength = int(data['ResponseMetadata']
                     ['HTTPHeaders']['content-length'])

    # Format: 2023-02-22 21:11:05.800895
    if dataLength > 5:
        storedLastMid = datetime.fromisoformat(data['Item']['lastMid'])
        storedNextMid = datetime.fromisoformat(data['Item']['nextMid'])
        storedSkipMid = datetime.fromisoformat(data['Item']['skipMid'])

    prefix = ""
    streak = 0
    personalRecord = 0

    currTime = datetime.now()
    lastMidnight = datetime.combine(currTime.date(), datetime.min.time())
    nextMidnight = lastMidnight + timedelta(days=1)
    skipMidnight = lastMidnight + timedelta(days=2)

    if dataLength < 5:
        prefix = "You just started a new streak! "

        put = table.put_item(
            Item={
                'id': str(ctx.user.id),
                'username': str(ctx.user.name),
                'streak': str(int(streak) + 1),
                'updated': str(currTime),
                'lastMid': str(lastMidnight),
                'nextMid': str(nextMidnight),
                'skipMid': str(skipMidnight),
                'personalRecord': str(int(personalRecord) + 1)
            }
        )

        streak = streak + 1

    elif currTime > storedSkipMid:
        prefix = "You missed your streak! "

        put = table.put_item(
            Item={
                'id': str(ctx.user.id),
                'username': str(ctx.user.name),
                'streak': str(int(streak) + 1),
                'updated': str(currTime),
                'lastMid': str(lastMidnight),
                'nextMid': str(nextMidnight),
                'skipMid': str(skipMidnight),
                'personalRecord': str(data['Item']['personalRecord'])
            }
        )

        streak = streak + 1

        if str(ctx.user.id) == str(dataCurrent['Item']['userId']):
            put = table.put_item(
                Item={
                    'id': 'currentStreak',
                    'stat': '0',
                    'username': 'MEGABOT',
                    'userId': '1077260321833635941'
                }
            )

            prefix = prefix + "**Current Highest Streak Reset!** "

    elif currTime > storedLastMid and currTime < storedNextMid:
        prefix = ""

        streak = int(data['Item']['streak'])

        put = table.put_item(
            Item={
                'id': str(ctx.user.id),
                'username': str(ctx.user.name),
                'streak': str(streak),
                'updated': str(currTime),
                'lastMid': str(data['Item']['lastMid']),
                'nextMid': str(data['Item']['nextMid']),
                'skipMid': str(data['Item']['skipMid']),
                'personalRecord': str(data['Item']['personalRecord'])
            }
        )

    elif currTime > storedLastMid and currTime > storedNextMid:
        prefix = "You hit your streak! "

        streak = int(data['Item']['streak']) + 1
        personalRecord = int(data['Item']['personalRecord'])

        if streak > personalRecord:
            personalRecord = streak

        put = table.put_item(
            Item={
                'id': str(ctx.user.id),
                'username': str(ctx.user.name),
                'streak': str(streak),
                'updated': str(currTime),
                'lastMid': str(lastMidnight),
                'nextMid': str(nextMidnight),
                'skipMid': str(skipMidnight),
                'personalRecord': str(personalRecord)
            }
        )

        if streak > int(dataStats['Item']['stat']):
            put = table.put_item(
                Item={
                    'id': 'allTimeStreak',
                    'stat': str(streak),
                    'username': str(ctx.user.name),
                    'userId': str(ctx.user.id)
                }
            )

        if streak > int(dataCurrent['Item']['stat']):
            put = table.put_item(
                Item={
                    'id': 'currentStreak',
                    'stat': str(streak),
                    'username': str(ctx.user.name),
                    'userId': str(ctx.user.id)
                }
            )

    if streak < 2:
        emote = "💩"
    elif streak < 3:
        emote = "✌️"
    elif streak < 4:
        emote = "👌"
    elif streak < 5:
        emote = "🍀"
    elif streak < 10:
        emote = "🔥"
    elif streak < 25:
        emote = "🧨"
    elif streak < 50:
        emote = "🏆"
    elif streak < 69:
        emote = "💀"
    elif streak < 70:
        emote = "-  *nice*."
    elif streak < 75:
        emote = "💀"
    elif streak < 100:
        emote = "💎"
    elif streak < 101:
        emote = "💯 - *Welcome to Party Mode*"
    else:
        emote = random_emoji()

    statMessage = ""

    if stats == "True":
        statMessage = "\n\n📊  __**Streak Stats**__\n**All-Time Highest Streak:** " + \
            str(dataStats['Item']['stat']) + \
            " *by* <@" + \
            str(dataStats['Item']['userId']) + \
            ">" + \
            "\n**Current Highest Streak:** " + \
            str(dataCurrent['Item']['stat']) + \
            " *by* <@" + \
            str(dataCurrent['Item']['userId']) + \
            ">" + \
            "\n**Personal Highest Streak:** " + \
            str(data['Item']['personalRecord']) + \
            " *by* <@" + \
            str(ctx.user.id) + ">"

    content = prefix + "Your streak is: " + \
        str(streak) + "  " + emote + statMessage

    await ctx.edit(content=f"{content}")
