#!/usr/bin/env python3
import boto3


async def loadMegacoinTable():
    TABLE = "discord-megacoin"
    ddb = boto3.resource("dynamodb")
    table = ddb.Table(TABLE)

    return table


async def add(user, coins):

    table = await loadMegacoinTable()

    data = table.get_item(Key={"id": str(user.id)})

    balance = 0

    dataLength = int(data["ResponseMetadata"]["HTTPHeaders"]["content-length"])
    if dataLength > 5:
        balance = int(data["Item"]["coins"])

    table.put_item(
        Item={
            "id": str(user.id),
            "username": str(user.name),
            "coins": str(balance + coins),
        }
    )


async def subtract(user, coins):

    table = await loadMegacoinTable()

    data = table.get_item(Key={"id": str(user.id)})

    balance = 0

    dataLength = int(data["ResponseMetadata"]["HTTPHeaders"]["content-length"])
    if dataLength > 5:
        balance = int(data["Item"]["coins"])

    table.put_item(
        Item={
            "id": str(user.id),
            "username": str(user.name),
            "coins": str(balance - coins),
        }
    )


async def balance(user):

    table = await loadMegacoinTable()

    data = table.get_item(Key={"id": str(user.id)})

    balance = 0

    dataLength = int(data["ResponseMetadata"]["HTTPHeaders"]["content-length"])
    if dataLength > 5:
        balance = int(data["Item"]["coins"])

    return balance
