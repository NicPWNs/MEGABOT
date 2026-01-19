import nacl from "tweetnacl";

/**
 * Verify Discord interaction signature
 * https://discord.com/developers/docs/interactions/receiving-and-responding#security-and-authorization
 */
export function verifyDiscordSignature(
  publicKey: string,
  signature: string,
  timestamp: string,
  body: string,
): boolean {
  try {
    return nacl.sign.detached.verify(
      Buffer.from(timestamp + body),
      Buffer.from(signature, "hex"),
      Buffer.from(publicKey, "hex"),
    );
  } catch (error) {
    console.error("Signature verification error:", error);
    return false;
  }
}
