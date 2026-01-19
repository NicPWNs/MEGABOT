// Application Command Definitions for Discord

export interface SlashCommand {
  name: string;
  description: string;
  options?: CommandOption[];
}

export interface CommandOption {
  name: string;
  description: string;
  type: CommandOptionType;
  required?: boolean;
  choices?: { name: string; value: string | number }[];
  min_value?: number;
  max_value?: number;
}

export enum CommandOptionType {
  SUB_COMMAND = 1,
  SUB_COMMAND_GROUP = 2,
  STRING = 3,
  INTEGER = 4,
  BOOLEAN = 5,
  USER = 6,
  CHANNEL = 7,
  ROLE = 8,
  MENTIONABLE = 9,
  NUMBER = 10,
  ATTACHMENT = 11,
}

// All registered commands
export const COMMANDS: SlashCommand[] = [
  // Utility Commands
  {
    name: "ping",
    description: "Responds with pong.",
  },
  {
    name: "version",
    description: "Return the latest MEGABOT version number.",
  },
  {
    name: "coin",
    description: "Flip a coin.",
  },
  {
    name: "dice",
    description: "Roll a dice.",
  },
  {
    name: "poll",
    description: "Create a poll with up to nine options.",
    options: [
      {
        name: "question",
        description: "Question to poll for.",
        type: CommandOptionType.STRING,
        required: true,
      },
      {
        name: "option1",
        description: "First option.",
        type: CommandOptionType.STRING,
        required: true,
      },
      {
        name: "option2",
        description: "Second option.",
        type: CommandOptionType.STRING,
        required: true,
      },
      {
        name: "option3",
        description: "Third option.",
        type: CommandOptionType.STRING,
        required: false,
      },
      {
        name: "option4",
        description: "Fourth option.",
        type: CommandOptionType.STRING,
        required: false,
      },
      {
        name: "option5",
        description: "Fifth option.",
        type: CommandOptionType.STRING,
        required: false,
      },
      {
        name: "option6",
        description: "Sixth option.",
        type: CommandOptionType.STRING,
        required: false,
      },
      {
        name: "option7",
        description: "Seventh option.",
        type: CommandOptionType.STRING,
        required: false,
      },
      {
        name: "option8",
        description: "Eighth option.",
        type: CommandOptionType.STRING,
        required: false,
      },
      {
        name: "option9",
        description: "Ninth option.",
        type: CommandOptionType.STRING,
        required: false,
      },
    ],
  },
  {
    name: "math",
    description: "Evaluate provided math expression.",
    options: [
      {
        name: "expression",
        description: "Expression to evaluate.",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },
  {
    name: "bless",
    description: "Blesses the mess!",
  },
  {
    name: "kanye",
    description: "Retrieve a random Kanye West quote.",
  },

  // MEGACOIN Commands
  {
    name: "balance",
    description: "View MEGACOIN balance.",
    options: [
      {
        name: "user",
        description: "User to get the balance of.",
        type: CommandOptionType.USER,
        required: false,
      },
    ],
  },
  {
    name: "bank",
    description: "View the MEGACOIN balance leaderboard.",
  },
  {
    name: "pay",
    description: "Pay another user some MEGACOIN.",
    options: [
      {
        name: "user",
        description: "User to pay.",
        type: CommandOptionType.USER,
        required: true,
      },
      {
        name: "amount",
        description: "Amount to pay.",
        type: CommandOptionType.INTEGER,
        required: true,
        min_value: 1,
      },
    ],
  },
  {
    name: "payout",
    description: "Payout MEGACOIN. (Admin only)",
    options: [
      {
        name: "user",
        description: "User to pay.",
        type: CommandOptionType.USER,
        required: true,
      },
      {
        name: "amount",
        description: "Amount to pay.",
        type: CommandOptionType.INTEGER,
        required: true,
      },
      {
        name: "message",
        description: "Message to send.",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },

  // Casino Commands
  {
    name: "blackjack",
    description: "Play blackjack.",
    options: [
      {
        name: "wager",
        description: "Amount you want to wager in blackjack.",
        type: CommandOptionType.INTEGER,
        required: true,
        min_value: 1,
      },
    ],
  },
  {
    name: "double",
    description: "Play MEGACOIN double or nothing.",
    options: [
      {
        name: "wager",
        description: "Amount you want to wager.",
        type: CommandOptionType.INTEGER,
        required: true,
        min_value: 1,
      },
    ],
  },
  {
    name: "wheel",
    description: "Spin the MEGACOIN wheel.",
    options: [
      {
        name: "wager",
        description: "Amount you want to wager.",
        type: CommandOptionType.INTEGER,
        required: true,
        min_value: 1,
      },
    ],
  },

  // Streak Command
  {
    name: "streak",
    description: "Keep a daily streak going!",
    options: [
      {
        name: "stats",
        description: "Get streak stats.",
        type: CommandOptionType.BOOLEAN,
        required: false,
      },
    ],
  },

  // External API Commands
  {
    name: "weather",
    description: "Seven day weather forecast.",
    options: [
      {
        name: "zipcode",
        description: "ZIP code for weather.",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },
  {
    name: "stock",
    description: "Searches a stock price.",
    options: [
      {
        name: "symbol",
        description: "Stock symbol to search for (ie. PLTR).",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },
  {
    name: "nasa",
    description: "Retrieve the NASA photo of the day.",
    options: [
      {
        name: "details",
        description: "Provide the explanation of the photo.",
        type: CommandOptionType.BOOLEAN,
        required: false,
      },
    ],
  },
  {
    name: "mc",
    description: "View the Minecraft Speed Running Leaderboard.",
  },

  // Photo Commands
  {
    name: "photo",
    description: "Return a random photo from the MEGABOT database.",
  },

  // GitHub Commands
  {
    name: "bug",
    description: "Report a MEGABOT bug.",
    options: [
      {
        name: "title",
        description: "Give the bug a title.",
        type: CommandOptionType.STRING,
        required: true,
      },
      {
        name: "description",
        description: "Describe the bug behavior.",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },
  {
    name: "feature",
    description: "Submit a MEGABOT feature request.",
    options: [
      {
        name: "title",
        description: "Give the feature request a title.",
        type: CommandOptionType.STRING,
        required: true,
      },
      {
        name: "description",
        description: "Describe the feature you desire.",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },

  // Emote Commands
  {
    name: "emote",
    description: "Search for a 7TV emote.",
    options: [
      {
        name: "search",
        description: "Emote to search for.",
        type: CommandOptionType.STRING,
        required: true,
      },
    ],
  },
];
