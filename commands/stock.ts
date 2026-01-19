import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getOptionValue } from "../handlers/commands";

export async function handleStock(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const symbol = getOptionValue<string>(interaction, "symbol")!.toUpperCase();
  const apiKey = process.env.STOCK_KEY;

  if (!apiKey) {
    return errorResponse("Stock API not configured.");
  }

  try {
    const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${apiKey}`;
    const response = await fetch(url);
    const data = (await response.json()) as {
      "Global Quote": Record<string, string>;
    };

    const quote = data["Global Quote"];
    if (!quote || !quote["01. symbol"]) {
      return errorResponse(`Could not find stock data for ${symbol}.`);
    }

    const stockSymbol = quote["01. symbol"];
    const price = parseFloat(quote["05. price"]).toFixed(2);
    const change = parseFloat(quote["09. change"]).toFixed(2);
    const changePercent = quote["10. change percent"];

    const isPositive = !change.startsWith("-");
    const emoji = isPositive ? "📈" : "📉";
    const color = isPositive ? Colors.GREEN : Colors.RED;

    return embedResponse({
      title: `${emoji} Stock Price of \`${stockSymbol}\` is $${price}`,
      description: `The price has changed by $${change} (${changePercent}) today.`,
      color,
    });
  } catch (error) {
    console.error("Stock API error:", error);
    return errorResponse("Failed to fetch stock data. Please try again later.");
  }
}
