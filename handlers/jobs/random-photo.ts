import { ScheduledEvent, Context } from "aws-lambda";
import { sendChannelMessage } from "../../utils/discord";
import { getRandomPhoto, getPhotoUrl } from "../../services/photos";
import { Colors } from "../../types/discord";

const MAIN_CHANNEL_ID = process.env.MAIN_CHANNEL_ID || "";

/**
 * Daily random photo job
 * Runs daily at 1 PM UTC
 */
export async function handler(
  event: ScheduledEvent,
  context: Context,
): Promise<void> {
  console.log("Running random photo job:", JSON.stringify(event));

  if (!MAIN_CHANNEL_ID) {
    console.log("MAIN_CHANNEL_ID not configured, skipping.");
    return;
  }

  try {
    // Get a random photo
    const photo = await getRandomPhoto();

    if (!photo) {
      console.log("No photos in database, skipping.");
      return;
    }

    // Get presigned URL
    const url = await getPhotoUrl(photo.name);

    // Send to channel
    await sendChannelMessage(MAIN_CHANNEL_ID, {
      embeds: [
        {
          title: "🌞 Random Photo of the Day",
          color: Colors.YELLOW,
          image: { url },
        },
      ],
    });

    console.log("Random photo posted successfully.");
  } catch (error) {
    console.error("Error in random photo job:", error);
    throw error;
  }
}
