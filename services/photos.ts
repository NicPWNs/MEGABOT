import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  GetCommand,
  PutCommand,
  ScanCommand,
} from "@aws-sdk/lib-dynamodb";
import {
  S3Client,
  GetObjectCommand,
  PutObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const dynamoClient = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(dynamoClient);
const s3Client = new S3Client({});

const PHOTOS_TABLE = process.env.PHOTOS_TABLE || "discord-photos";
const PHOTO_BUCKET = process.env.PHOTO_BUCKET || "";

export interface PhotoData {
  id: string;
  name: string;
  type: string;
}

/**
 * Get all photos from the database
 */
export async function getAllPhotos(): Promise<PhotoData[]> {
  const response = await docClient.send(
    new ScanCommand({
      TableName: PHOTOS_TABLE,
    }),
  );

  if (!response.Items) {
    return [];
  }

  return response.Items.map((item) => ({
    id: item.id as string,
    name: item.name as string,
    type: item.type as string,
  }));
}

/**
 * Get a random photo from the database
 */
export async function getRandomPhoto(): Promise<PhotoData | null> {
  const photos = await getAllPhotos();

  if (photos.length === 0) {
    return null;
  }

  const randomIndex = Math.floor(Math.random() * photos.length);
  return photos[randomIndex];
}

/**
 * Get a presigned URL for a photo
 */
export async function getPhotoUrl(photoName: string): Promise<string> {
  const command = new GetObjectCommand({
    Bucket: PHOTO_BUCKET,
    Key: photoName,
  });

  // URL expires in 7 days (604800 seconds)
  return await getSignedUrl(s3Client, command, { expiresIn: 604800 });
}

/**
 * Save a photo record to the database
 */
export async function savePhotoRecord(
  id: string,
  name: string,
  type: string,
): Promise<void> {
  await docClient.send(
    new PutCommand({
      TableName: PHOTOS_TABLE,
      Item: {
        id,
        name,
        type,
      },
    }),
  );
}

/**
 * Upload a photo to S3 and save the record
 */
export async function uploadPhoto(
  id: string,
  name: string,
  type: string,
  body: Buffer,
): Promise<string> {
  // Upload to S3
  await s3Client.send(
    new PutObjectCommand({
      Bucket: PHOTO_BUCKET,
      Key: name,
      Body: body,
      ContentType: type,
    }),
  );

  // Save record to DynamoDB
  await savePhotoRecord(id, name, type);

  // Return presigned URL
  return await getPhotoUrl(name);
}

/**
 * Supported photo/video types
 */
export const SUPPORTED_TYPES = [
  "image/jpeg",
  "image/png",
  "image/heic",
  "video/quicktime",
  "video/mp4",
];

/**
 * Check if a content type is supported
 */
export function isSupportedType(contentType: string): boolean {
  return SUPPORTED_TYPES.includes(contentType);
}
