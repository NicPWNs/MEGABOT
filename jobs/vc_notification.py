import logging
import threading
import time
import discord

logger = logging.getLogger('LOGGER')

# Track & Notify when users enter/leave voice channels

async def vc_notification(bot, member, before, after, cooldownUsersSet):
    
   guild = discord.utils.get(bot.guilds, name="MEGACORD")
   channel = discord.utils.get(guild.channels, name="bot-testing")

   # Anti-Spam Cooldown Check
   if member.id in cooldownUsersSet:
      return

   # notify text-channel & give user spam cooldown
   if before.channel is None:
      logger.info(f" Voice-Channel-Notifcation: {member.id} added to activeUsersSet for 10 minutes.")
            
      cooldownUsersSet.add(member.id)
      timer = threading.Thread(target = vc_notif_set_remove, args=(cooldownUsersSet, member.id, 600))
      timer.start()

      # Special notification for MEGALORD roles
      role = discord.utils.get(guild.roles, name="MEGALORDS")
      if role in member.roles:
         await channel.send(f"*MEGALORD* <@{member.id}> **joined** <#{after.channel.id}>. Alerting @everyone")
      else:
         await channel.send(f"<@{member.id}> **joined** <#{after.channel.id}>")

      # Left Notifcation -- Maybe add delay to check if they rejoined a VC.. if not after ~10 mins, display they left
      # elif after.channel is None:
      #     print(member.name + ' left')
      #     await channel.send(f"<@{member.id}> **left** <#{before.channel.id}>")

   return

# Remove users from cooldownUsersSet
def vc_notif_set_remove(set, user, ttl):
   time.sleep(ttl)
   logger.info(f"Voice-Channel-Notifcation: User {user} cooldown removed")
   set.remove(user)

