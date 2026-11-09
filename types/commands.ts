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
  min_length?: number;
  max_length?: number;
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

export const COLOR_PALETTE = [
  { name: "Teal", value: "teal", color: 0x1abc9c },
  { name: "Green", value: "green", color: 0x2ecc71 },
  { name: "Blue", value: "blue", color: 0x3498db },
  { name: "Purple", value: "purple", color: 0x9b59b6 },
  { name: "Pink", value: "pink", color: 0xe91e63 },
  { name: "Yellow", value: "yellow", color: 0xf1c40f },
  { name: "Orange", value: "orange", color: 0xe67e22 },
  { name: "Red", value: "red", color: 0xe74c3c },
  { name: "Silver", value: "silver", color: 0x95a5a6 },
  { name: "Blue Gray", value: "blue-gray", color: 0x607d8b },
  { name: "Rose", value: "rose", color: 0xe35484 },
  { name: "Coral", value: "coral", color: 0xe25e32 },
  { name: "Gold", value: "gold", color: 0xa4850a },
  { name: "Lime", value: "lime", color: 0x409c21 },
  { name: "Emerald", value: "emerald", color: 0x239a54 },
  { name: "Mint", value: "mint", color: 0x3a9875 },
  { name: "Jade", value: "jade", color: 0x1c9c71 },
  { name: "Turquoise", value: "turquoise", color: 0x1b987f },
  { name: "Sky Blue", value: "sky-blue", color: 0x2391c7 },
] as const;

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
        max_length: 300,
        required: true,
      },
      {
        name: "option1",
        description: "First option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: true,
      },
      {
        name: "option2",
        description: "Second option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: true,
      },
      {
        name: "option3",
        description: "Third option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "option4",
        description: "Fourth option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "option5",
        description: "Fifth option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "option6",
        description: "Sixth option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "option7",
        description: "Seventh option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "option8",
        description: "Eighth option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "option9",
        description: "Ninth option.",
        type: CommandOptionType.STRING,
        max_length: 55,
        required: false,
      },
      {
        name: "hours",
        description: "How long the poll stays open, in hours (default 24).",
        type: CommandOptionType.INTEGER,
        required: false,
        min_value: 1,
        max_value: 768,
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
    description: "Payout MEGACOIN. (MEGALORDS only)",
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
  {
    name: "color",
    description: "Set your name color.",
    options: [
      {
        name: "color",
        description: "Choose a color from the palette.",
        type: CommandOptionType.STRING,
        required: true,
        choices: COLOR_PALETTE.map(({ name, value }) => ({ name, value })),
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
