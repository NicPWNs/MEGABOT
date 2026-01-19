import {
  DiscordInteraction,
  InteractionResponse,
  Colors,
  MEGACOIN_EMOJI,
  ButtonStyle,
  MessageComponentData,
} from "../types/discord";
import {
  embedResponse,
  errorResponse,
  updateResponse,
  createButtonRow,
} from "../utils/discord";
import { getOptionValue, getUser } from "../handlers/commands";
import { getBalance, addCoins, subtractCoins } from "../services/megacoin";

// Card suits and values
const SUITS = ["c", "d", "h", "s"]; // clubs, diamonds, hearts, spades
const VALUES = [
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "j",
  "q",
  "k",
  "a",
];

const CARD_BACK = "🂠";

interface Card {
  value: string;
  suit: string;
}

interface BlackjackState {
  dealerHand: Card[];
  playerHand: Card[];
  wager: number;
  double: number;
  userId: string;
  username: string;
}

// In-memory game state (for serverless, you'd want to store this in DynamoDB)
// For now, we encode the state in the custom_id
function encodeState(state: BlackjackState): string {
  return Buffer.from(JSON.stringify(state)).toString("base64");
}

function decodeState(encoded: string): BlackjackState {
  return JSON.parse(Buffer.from(encoded, "base64").toString("utf-8"));
}

function getRandomCard(usedCards: Card[]): Card {
  let card: Card;
  do {
    card = {
      value: VALUES[Math.floor(Math.random() * VALUES.length)],
      suit: SUITS[Math.floor(Math.random() * SUITS.length)],
    };
  } while (
    usedCards.some((c) => c.value === card.value && c.suit === card.suit)
  );
  return card;
}

function calculateHandValue(hand: Card[]): number {
  let total = 0;
  let aces = 0;

  for (const card of hand) {
    if (["j", "q", "k"].includes(card.value)) {
      total += 10;
    } else if (card.value === "a") {
      total += 11;
      aces++;
    } else {
      total += parseInt(card.value, 10);
    }
  }

  // Adjust for aces
  while (total > 21 && aces > 0) {
    total -= 10;
    aces--;
  }

  return total;
}

function formatHand(hand: Card[], hideSecond = false): string {
  return hand
    .map((card, index) => {
      if (hideSecond && index === 1) {
        return CARD_BACK;
      }
      // Use text representation for card display
      const valueDisplay = card.value.toUpperCase();
      const suitEmoji =
        card.suit === "h"
          ? "♥️"
          : card.suit === "d"
            ? "♦️"
            : card.suit === "c"
              ? "♣️"
              : "♠️";
      return `[${valueDisplay}${suitEmoji}]`;
    })
    .join(" ");
}

export async function handleBlackjack(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const wager = getOptionValue<number>(interaction, "wager")!;
  const user = getUser(interaction);

  // Validation (matches Python: wager < 0 check)
  if (wager < 0) {
    return embedResponse({
      title: "🃏 Blackjack",
      description: "🤡 Nice try.",
      color: Colors.PURPLE,
    });
  }

  const balance = await getBalance(user.id);

  if (balance === 0) {
    return embedResponse({
      title: "🃏 Blackjack",
      description: `You have 0 ${MEGACOIN_EMOJI}`,
      color: Colors.PURPLE,
    });
  }

  if (balance < wager) {
    return embedResponse({
      title: "🃏 Blackjack",
      description: `You don't have ${wager} ${MEGACOIN_EMOJI}`,
      color: Colors.PURPLE,
    });
  }

  // Deal initial cards
  const usedCards: Card[] = [];
  const dealerHand: Card[] = [];
  const playerHand: Card[] = [];

  // Deal 2 cards each
  dealerHand.push(getRandomCard(usedCards));
  usedCards.push(dealerHand[0]);
  dealerHand.push(getRandomCard(usedCards));
  usedCards.push(dealerHand[1]);

  playerHand.push(getRandomCard(usedCards));
  usedCards.push(playerHand[0]);
  playerHand.push(getRandomCard(usedCards));
  usedCards.push(playerHand[1]);

  const dealerValue = calculateHandValue(dealerHand);
  const playerValue = calculateHandValue(playerHand);

  // Check for immediate blackjacks
  if (playerValue === 21 && dealerValue === 21) {
    // Push
    return embedResponse({
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(dealerHand)} (${dealerValue})\n**You:** ${formatHand(playerHand)} (${playerValue})\n\n➡️ **Push!** Dealer and <@${user.id}> both have Blackjack!`,
      color: Colors.PURPLE,
      footer: {
        text: "+ 0",
        icon_url:
          "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
      },
    });
  }

  if (playerValue === 21) {
    // Player blackjack - wins 2x
    await addCoins(user.id, user.username, wager * 2);
    return embedResponse({
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(dealerHand)} (${dealerValue})\n**You:** ${formatHand(playerHand)} (${playerValue})\n\n✅ **Win!** <@${user.id}> has Blackjack!`,
      color: Colors.PURPLE,
      footer: {
        text: `+ ${wager * 2}`,
        icon_url:
          "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
      },
    });
  }

  if (dealerValue === 21) {
    // Dealer blackjack
    await subtractCoins(user.id, user.username, wager);
    return embedResponse({
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(dealerHand)} (${dealerValue})\n**You:** ${formatHand(playerHand)} (${playerValue})\n\n❌ **Loss!** Dealer has Blackjack!`,
      color: Colors.PURPLE,
      footer: {
        text: `- ${wager}`,
        icon_url:
          "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
      },
    });
  }

  // Create game state
  const state: BlackjackState = {
    dealerHand,
    playerHand,
    wager,
    double: 1,
    userId: user.id,
    username: user.username,
  };

  const encodedState = encodeState(state);

  // Can double down?
  const canDouble = balance >= wager * 2;

  const buttons = [
    {
      customId: `blackjack_hit_${encodedState}`,
      label: "Hit",
      style: ButtonStyle.SUCCESS,
      emoji: "🟢",
    },
    {
      customId: `blackjack_stand_${encodedState}`,
      label: "Stand",
      style: ButtonStyle.DANGER,
      emoji: "🛑",
    },
  ];

  if (canDouble) {
    buttons.push({
      customId: `blackjack_double_${encodedState}`,
      label: "Double",
      style: ButtonStyle.PRIMARY,
      emoji: "⏫",
    });
  }

  return embedResponse(
    {
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(dealerHand, true)} (?)\n**You:** ${formatHand(playerHand)} (${playerValue})\n\n**Hit** 🟢 or **Stand** 🛑${canDouble ? " or **Double** ⏫" : ""}?`,
      color: Colors.PURPLE,
    },
    false,
    [createButtonRow(buttons)],
  );
}

export async function handleBlackjackComponent(
  interaction: DiscordInteraction,
): Promise<InteractionResponse> {
  const data = interaction.data as MessageComponentData;
  const customId = data.custom_id;
  const user = getUser(interaction);

  // Parse the action and state
  const parts = customId.split("_");
  const action = parts[1]; // hit, stand, or double
  const encodedState = parts.slice(2).join("_");

  let state: BlackjackState;
  try {
    state = decodeState(encodedState);
  } catch (error) {
    return errorResponse("Game state expired. Please start a new game.");
  }

  // Verify this is the correct player
  if (state.userId !== user.id) {
    return errorResponse("This isn't your game!");
  }

  const usedCards = [...state.dealerHand, ...state.playerHand];

  // Handle actions
  if (action === "double") {
    // Double down - one card and stand
    state.double = 2;
    const newCard = getRandomCard(usedCards);
    state.playerHand.push(newCard);
  } else if (action === "hit") {
    // Hit - draw a card
    const newCard = getRandomCard(usedCards);
    state.playerHand.push(newCard);
  }

  const playerValue = calculateHandValue(state.playerHand);
  const dealerValue = calculateHandValue(state.dealerHand);

  // Check for bust
  if (playerValue > 21) {
    await subtractCoins(
      state.userId,
      state.username,
      state.wager * state.double,
    );
    return updateResponse({
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(state.dealerHand)} (${dealerValue})\n**You:** ${formatHand(state.playerHand)} (${playerValue})\n\n❌ **Loss!** <@${state.userId}> busted with ${playerValue}!`,
      color: Colors.PURPLE,
      footer: {
        text: `- ${state.wager * state.double}`,
        icon_url:
          "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
      },
    });
  }

  // If doubled or standing, dealer plays
  if (action === "stand" || action === "double") {
    // Dealer draws until 17+
    while (calculateHandValue(state.dealerHand) < 17) {
      const newCard = getRandomCard([...usedCards, ...state.dealerHand]);
      state.dealerHand.push(newCard);
    }

    const finalDealerValue = calculateHandValue(state.dealerHand);

    // Determine winner
    if (finalDealerValue > 21) {
      // Dealer busts
      await addCoins(state.userId, state.username, state.wager * state.double);
      return updateResponse({
        title: "🃏 Blackjack",
        description: `**Dealer:** ${formatHand(state.dealerHand)} (${finalDealerValue})\n**You:** ${formatHand(state.playerHand)} (${playerValue})\n\n✅ **Win!** Dealer busted!`,
        color: Colors.PURPLE,
        footer: {
          text: `+ ${state.wager * state.double}`,
          icon_url:
            "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
        },
      });
    }

    if (playerValue > finalDealerValue) {
      // Player wins
      await addCoins(state.userId, state.username, state.wager * state.double);
      return updateResponse({
        title: "🃏 Blackjack",
        description: `**Dealer:** ${formatHand(state.dealerHand)} (${finalDealerValue})\n**You:** ${formatHand(state.playerHand)} (${playerValue})\n\n✅ **Win!** <@${state.userId}> beats Dealer!`,
        color: Colors.PURPLE,
        footer: {
          text: `+ ${state.wager * state.double}`,
          icon_url:
            "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
        },
      });
    }

    if (finalDealerValue > playerValue) {
      // Dealer wins
      await subtractCoins(
        state.userId,
        state.username,
        state.wager * state.double,
      );
      return updateResponse({
        title: "🃏 Blackjack",
        description: `**Dealer:** ${formatHand(state.dealerHand)} (${finalDealerValue})\n**You:** ${formatHand(state.playerHand)} (${playerValue})\n\n❌ **Loss!** Dealer beats <@${state.userId}>!`,
        color: Colors.PURPLE,
        footer: {
          text: `- ${state.wager * state.double}`,
          icon_url:
            "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
        },
      });
    }

    // Push
    return updateResponse({
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(state.dealerHand)} (${finalDealerValue})\n**You:** ${formatHand(state.playerHand)} (${playerValue})\n\n➡️ **Push!** Dealer and <@${state.userId}> are tied.`,
      color: Colors.PURPLE,
      footer: {
        text: "+ 0",
        icon_url:
          "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
      },
    });
  }

  // Player can continue hitting
  const newEncodedState = encodeState(state);
  const buttons = [
    {
      customId: `blackjack_hit_${newEncodedState}`,
      label: "Hit",
      style: ButtonStyle.SUCCESS,
      emoji: "🟢",
    },
    {
      customId: `blackjack_stand_${newEncodedState}`,
      label: "Stand",
      style: ButtonStyle.DANGER,
      emoji: "🛑",
    },
  ];

  return updateResponse(
    {
      title: "🃏 Blackjack",
      description: `**Dealer:** ${formatHand(state.dealerHand, true)} (?)\n**You:** ${formatHand(state.playerHand)} (${playerValue})\n\n**Hit** 🟢 or **Stand** 🛑?`,
      color: Colors.PURPLE,
    },
    [createButtonRow(buttons)],
  );
}
