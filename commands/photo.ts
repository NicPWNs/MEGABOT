import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getRandomPhoto, getPhotoUrl } from "../services/photos";

export async function handlePhoto(
  _interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  try {
    const photo = await getRandomPhoto();

    if (!photo) {
      return errorResponse("No photos in the database yet!");
    }

    const url = await getPhotoUrl(photo.name);

    return embedResponse({
      title: "📸 Random Photo",
      color: Colors.YELLOW,
      image: { url },
    });
  } catch (error) {
    console.error("Photo error:", error);
    return errorResponse("Failed to fetch a random photo.");
  }
}
