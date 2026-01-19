import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
} from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

const STREAK_TABLE = process.env.STREAK_TABLE || "discord-streak";

export interface StreakData {
  id: string;
  username: string;
  streak: number;
  updated: string;
  lastMid: string;
  nextMid: string;
  skipMid: string;
  personalRecord: number;
}

export interface StreakStats {
  allTimeStreak: { stat: number; username: string; userId: string };
  currentStreak: { stat: number; username: string; userId: string };
}

/**
 * Get a user's streak data
 */
export async function getStreakData(
  userId: string,
): Promise<StreakData | null> {
  const response = await docClient.send(
    new GetCommand({
      TableName: STREAK_TABLE,
      Key: { id: userId },
    }),
  );

  if (!response.Item) {
    return null;
  }

  return {
    id: response.Item.id as string,
    username: response.Item.username as string,
    streak: parseInt(response.Item.streak as string, 10) || 0,
    updated: response.Item.updated as string,
    lastMid: response.Item.lastMid as string,
    nextMid: response.Item.nextMid as string,
    skipMid: response.Item.skipMid as string,
    personalRecord: parseInt(response.Item.personalRecord as string, 10) || 0,
  };
}

/**
 * Get streak stats (all-time and current)
 */
export async function getStreakStats(): Promise<StreakStats> {
  const [allTimeResponse, currentResponse] = await Promise.all([
    docClient.send(
      new GetCommand({
        TableName: STREAK_TABLE,
        Key: { id: "allTimeStreak" },
      }),
    ),
    docClient.send(
      new GetCommand({
        TableName: STREAK_TABLE,
        Key: { id: "currentStreak" },
      }),
    ),
  ]);

  return {
    allTimeStreak: {
      stat: parseInt(allTimeResponse.Item?.stat as string, 10) || 0,
      username: (allTimeResponse.Item?.username as string) || "Unknown",
      userId: (allTimeResponse.Item?.userId as string) || "",
    },
    currentStreak: {
      stat: parseInt(currentResponse.Item?.stat as string, 10) || 0,
      username: (currentResponse.Item?.username as string) || "Unknown",
      userId: (currentResponse.Item?.userId as string) || "",
    },
  };
}

/**
 * Update a user's streak
 */
export async function updateStreak(
  userId: string,
  username: string,
  streak: number,
  personalRecord: number,
  lastMid: Date,
  nextMid: Date,
  skipMid: Date,
): Promise<void> {
  await docClient.send(
    new PutCommand({
      TableName: STREAK_TABLE,
      Item: {
        id: userId,
        username: username,
        streak: streak.toString(),
        updated: new Date().toISOString(),
        lastMid: lastMid.toISOString(),
        nextMid: nextMid.toISOString(),
        skipMid: skipMid.toISOString(),
        personalRecord: personalRecord.toString(),
      },
    }),
  );
}

/**
 * Update streak stats
 */
export async function updateStreakStats(
  type: "allTimeStreak" | "currentStreak",
  stat: number,
  username: string,
  userId: string,
): Promise<void> {
  await docClient.send(
    new PutCommand({
      TableName: STREAK_TABLE,
      Item: {
        id: type,
        stat: stat.toString(),
        username: username,
        userId: userId,
      },
    }),
  );
}

/**
 * Process a streak hit and return the result
 */
export async function processStreak(
  userId: string,
  username: string,
  botUserId: string,
  botUsername: string,
): Promise<{
  streak: number;
  personalRecord: number;
  prefix: string;
  hit: boolean;
  isNewRecord: boolean;
}> {
  const now = new Date();
  const lastMidnight = new Date(now);
  lastMidnight.setHours(0, 0, 0, 0);

  const nextMidnight = new Date(lastMidnight);
  nextMidnight.setDate(nextMidnight.getDate() + 1);

  const skipMidnight = new Date(lastMidnight);
  skipMidnight.setDate(skipMidnight.getDate() + 2);

  const existingData = await getStreakData(userId);
  const stats = await getStreakStats();

  let streak = 0;
  let personalRecord = 0;
  let prefix = "";
  let hit = false;
  let isNewRecord = false;

  if (!existingData) {
    // New user starting a streak
    prefix = "You just started a new streak! ";
    hit = true;
    streak = 1;
    personalRecord = 1;
    isNewRecord = true;

    await updateStreak(
      userId,
      username,
      streak,
      personalRecord,
      lastMidnight,
      nextMidnight,
      skipMidnight,
    );
  } else {
    const storedSkipMid = new Date(existingData.skipMid);
    const storedNextMid = new Date(existingData.nextMid);
    const storedLastMid = new Date(existingData.lastMid);

    if (now > storedSkipMid) {
      // Missed streak
      prefix = "You missed your streak! ";
      hit = true;
      streak = 1;
      personalRecord = existingData.personalRecord;

      await updateStreak(
        userId,
        username,
        streak,
        personalRecord,
        lastMidnight,
        nextMidnight,
        skipMidnight,
      );

      // Reset current streak if they were the leader
      if (stats.currentStreak.userId === userId) {
        await updateStreakStats("currentStreak", 0, botUsername, botUserId);
        prefix += "**Current Highest Streak Reset!** ";
      }
    } else if (now > storedLastMid && now < storedNextMid) {
      // Already hit today
      prefix = "";
      streak = existingData.streak;
      personalRecord = existingData.personalRecord;
    } else if (now >= storedNextMid && now < storedSkipMid) {
      // Valid streak continuation (matches Python: currTime > storedLastMid and currTime > storedNextMid)
      prefix = "You hit your streak! ";
      hit = true;
      streak = existingData.streak + 1;
      personalRecord = Math.max(existingData.personalRecord, streak);
      isNewRecord = streak > existingData.personalRecord;

      await updateStreak(
        userId,
        username,
        streak,
        personalRecord,
        lastMidnight,
        nextMidnight,
        skipMidnight,
      );

      // Update current streak if this is the new high
      if (streak > stats.currentStreak.stat) {
        await updateStreakStats("currentStreak", streak, username, userId);
      }

      // Update all-time streak if this is the new record (Python doesn't add special text)
      if (streak > stats.allTimeStreak.stat) {
        await updateStreakStats("allTimeStreak", streak, username, userId);
      }
    } else {
      // Edge case: before lastMid
      prefix = "";
      streak = existingData.streak;
      personalRecord = existingData.personalRecord;
    }
  }

  return { streak, personalRecord, prefix, hit, isNewRecord };
}
