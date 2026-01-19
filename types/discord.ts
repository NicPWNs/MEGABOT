// Discord API Types for Serverless Bot

export interface DiscordInteraction {
  id: string;
  application_id: string;
  type: InteractionType;
  data?: ApplicationCommandData | MessageComponentData;
  guild_id?: string;
  channel_id?: string;
  member?: GuildMember;
  user?: DiscordUser;
  token: string;
  version: number;
  message?: DiscordMessage;
}

export interface ApplicationCommandData {
  id: string;
  name: string;
  type: number;
  options?: InteractionCommandOption[];
  resolved?: ResolvedData;
}

export interface ResolvedData {
  users?: Record<string, DiscordUser>;
  members?: Record<string, Partial<GuildMember>>;
  roles?: Record<string, unknown>;
  channels?: Record<string, unknown>;
}

export interface MessageComponentData {
  custom_id: string;
  component_type: ComponentType;
  values?: string[];
}

export interface InteractionCommandOption {
  name: string;
  type: number;
  value?: string | number | boolean;
  options?: InteractionCommandOption[];
}

export interface GuildMember {
  user: DiscordUser;
  nick?: string;
  roles: string[];
  premium_since?: string;
}

export interface DiscordUser {
  id: string;
  username: string;
  discriminator: string;
  global_name?: string;
  avatar?: string;
}

export interface DiscordMessage {
  id: string;
  channel_id: string;
  content: string;
  embeds?: DiscordEmbed[];
  components?: ActionRow[];
}

export interface DiscordEmbed {
  title?: string;
  description?: string;
  color?: number;
  footer?: { text: string; icon_url?: string };
  image?: { url: string };
  thumbnail?: { url: string };
  fields?: { name: string; value: string; inline?: boolean }[];
}

export interface ActionRow {
  type: 1;
  components: (ButtonComponent | SelectMenuComponent)[];
}

export interface ButtonComponent {
  type: 2;
  style: ButtonStyle;
  label?: string;
  emoji?: { name: string; id?: string };
  custom_id?: string;
  url?: string;
  disabled?: boolean;
}

export interface SelectMenuComponent {
  type: 3;
  custom_id: string;
  options: SelectOption[];
  placeholder?: string;
  disabled?: boolean;
}

export interface SelectOption {
  label: string;
  value: string;
  description?: string;
  emoji?: { name: string; id?: string };
  default?: boolean;
}

export enum InteractionType {
  PING = 1,
  APPLICATION_COMMAND = 2,
  MESSAGE_COMPONENT = 3,
  APPLICATION_COMMAND_AUTOCOMPLETE = 4,
  MODAL_SUBMIT = 5,
}

export enum InteractionResponseType {
  PONG = 1,
  CHANNEL_MESSAGE_WITH_SOURCE = 4,
  DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5,
  DEFERRED_UPDATE_MESSAGE = 6,
  UPDATE_MESSAGE = 7,
  APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8,
  MODAL = 9,
}

export enum ComponentType {
  ACTION_ROW = 1,
  BUTTON = 2,
  STRING_SELECT = 3,
}

export enum ButtonStyle {
  PRIMARY = 1,
  SECONDARY = 2,
  SUCCESS = 3,
  DANGER = 4,
  LINK = 5,
}

export interface InteractionResponse {
  type: InteractionResponseType;
  data?: InteractionResponseData;
}

export interface InteractionResponseData {
  content?: string;
  embeds?: DiscordEmbed[];
  components?: ActionRow[];
  flags?: number;
  tts?: boolean;
}

// Message Flags
export const MessageFlags = {
  EPHEMERAL: 64,
};

// Colors for embeds
export const Colors = {
  PURPLE: 0x9366cd,
  GOLD: 0xfee9b6,
  YELLOW: 0xffcc4d,
  GREEN: 0x77b354,
  RED: 0xdd2f45,
  BLUE: 0x5965f3,
  ORANGE: 0xffad32,
};

// MEGACOIN emoji reference
export const MEGACOIN_EMOJI = "<:MEGACOIN:1090620048621707324>";
export const MEGACARD_EMOJI = "<:MEGACARD:1091828635138281482>";
