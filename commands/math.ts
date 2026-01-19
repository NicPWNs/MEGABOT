import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
} from "../types/discord";
import { embedResponse, errorResponse } from "../utils/discord";
import { getOptionValue } from "../handlers/commands";

export async function handleMath(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const expression = getOptionValue<string>(interaction, "expression");

  if (!expression) {
    return errorResponse("Please provide a math expression.");
  }

  try {
    // Sanitize the expression - only allow safe math characters
    const sanitized = expression.replace(/[^0-9+\-*/().%^\s]/g, "");

    if (sanitized !== expression.replace(/\s/g, "").replace(/x/gi, "*")) {
      return errorResponse(
        "Invalid characters in expression. Only numbers and +, -, *, /, (, ), %, ^ are allowed.",
      );
    }

    // Replace common math symbols
    const prepared = sanitized
      .replace(/\^/g, "**") // Exponentiation
      .replace(/x/gi, "*"); // Allow x for multiplication

    // Evaluate safely using Function constructor (safer than eval)
    const result = Function(`"use strict"; return (${prepared})`)();

    if (typeof result !== "number" || !isFinite(result)) {
      return errorResponse("Invalid mathematical expression.");
    }

    return embedResponse({
      title: "🧮 Math Result",
      description: `\`${expression}\` = **${result}**`,
      color: Colors.BLUE,
    });
  } catch (error) {
    console.error("Math evaluation error:", error);
    return errorResponse(
      "Could not evaluate the expression. Please check your syntax.",
    );
  }
}
