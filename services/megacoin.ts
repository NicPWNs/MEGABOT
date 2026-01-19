import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  ScanCommand,
} from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const MEGACOIN_TABLE = process.env.MEGACOIN_TABLE || "discord-megacoin";

export interface MegacoinUser {
  id: string;
  username: string;
  coins: number;
}

/**
 * Get a user's MEGACOIN balance
 */
export async function getBalance(userId: string): Promise<number> {
  const response = await docClient.send(
    new GetCommand({
      TableName: MEGACOIN_TABLE,
      Key: { id: userId },
    }),
  );

  if (!response.Item) {
    return 0;
  }

  return parseInt(response.Item.coins as string, 10) || 0;
}

/**
 * Add MEGACOIN to a user's balance
 */
export async function addCoins(
  userId: string,
  username: string,
  amount: number,
): Promise<number> {
  const currentBalance = await getBalance(userId);
  const newBalance = currentBalance + amount;

  await docClient.send(
    new PutCommand({
      TableName: MEGACOIN_TABLE,
      Item: {
        id: userId,
        username: username,
        coins: newBalance.toString(),
      },
    }),
  );

  return newBalance;
}

/**
 * Subtract MEGACOIN from a user's balance
 */
export async function subtractCoins(
  userId: string,
  username: string,
  amount: number,
): Promise<number> {
  const currentBalance = await getBalance(userId);
  const newBalance = Math.max(0, currentBalance - amount);

  await docClient.send(
    new PutCommand({
      TableName: MEGACOIN_TABLE,
      Item: {
        id: userId,
        username: username,
        coins: newBalance.toString(),
      },
    }),
  );

  return newBalance;
}

/**
 * Get all users sorted by balance (leaderboard)
 */
export async function getLeaderboard(): Promise<MegacoinUser[]> {
  const response = await docClient.send(
    new ScanCommand({
      TableName: MEGACOIN_TABLE,
    }),
  );

  if (!response.Items) {
    return [];
  }

  const users: MegacoinUser[] = response.Items.map((item) => ({
    id: item.id as string,
    username: item.username as string,
    coins: parseInt(item.coins as string, 10) || 0,
  }));

  // Sort by coins descending
  return users.sort((a, b) => b.coins - a.coins).filter((u) => u.coins > 0);
}

/**
 * Transfer coins between users
 */
export async function transferCoins(
  fromUserId: string,
  fromUsername: string,
  toUserId: string,
  toUsername: string,
  amount: number,
): Promise<{ success: boolean; message: string }> {
  const fromBalance = await getBalance(fromUserId);

  if (fromBalance < amount) {
    return {
      success: false,
      message: `You don't have ${amount} MEGACOIN to transfer.`,
    };
  }

  await subtractCoins(fromUserId, fromUsername, amount);
  await addCoins(toUserId, toUsername, amount);

  return {
    success: true,
    message: `Successfully transferred ${amount} MEGACOIN.`,
  };
}
