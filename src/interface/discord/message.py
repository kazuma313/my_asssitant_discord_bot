import discord
import os
from src.application.usecases.calling_agent import (free_chat,
                                                    klasifikasi_bad_word)
from discord.ext import commands

description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""
secret_role = "explorer"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", description=description, intents=intents)

  
async def handle_bad_words(message):
    """Mengurus pengecekan kata kasar dan penghapusan pesan."""
    try:
        print(f"Sedang mengecek bad word: '{message.content}'")
        is_bad_word = await klasifikasi_bad_word(text_to_check=message.content)
        
        if str(is_bad_word).lower() == "yes":
            await message.delete()
            await message.channel.send(f"Please mind your manner!!! - {message.author.mention}")
            print("Pesan buruk dihapus.")
            return True # Berhasil mendeteksi bad word
    except Exception as e:
        print(f"Error di fungsi klasifikasi_bad_word: {e}")
    
    return False

async def handle_ai_chat(message):
    """Mengurus respons AI saat bot di-mention."""
    if bot.user.mentioned_in(message): # type: ignore
        print("Bot di-mention, memproses jawaban...")
        # Bersihkan mention dari teks
        clean_content = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()

        if clean_content == "":
            await message.channel.send(f"Halo {message.author.mention}! Ada yang bisa saya bantu?")
            return

        loading_msg = await message.reply("⏳ Memproses pertanyaanmu...")
        try:
            ai_response = await free_chat(clean_content)
            content_to_send = ai_response.content if hasattr(ai_response, 'content') else ai_response
            await message.reply(str(content_to_send))
            await loading_msg.delete()
        except Exception as e:
            print(f"Error AI: {e}")
            await loading_msg.edit(content="Maaf, terjadi kendala teknis.")


async def send_summary_to_users(
    interaction: discord.Interaction, url: str, summary: str
) -> None:
    """
    Send summary messages to appropriate users based on who requested it.
    Uses MessageConfig to determine user permissions and routing.

    Args:
        interaction: Discord interaction object
        url: The YouTube URL that was summarized
        summary: The actual summary content
    """
    requester_name = interaction.user.name

    try:
        if message_config.is_primary_user(requester_name):
            await _send_dm_to_user(interaction.user, url, summary, is_own_request=True) # type: ignore
        else:
            await _send_to_multiple_users(interaction, url, summary, requester_name)

        await interaction.followup.send("Summary sent to your DMs!", ephemeral=True)

    except discord.Forbidden:
        await interaction.followup.send(
            "I couldn't send you a DM. Please check if you have DMs enabled from server members.",
            ephemeral=True,
        )
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


async def _send_dm_to_user(
    user: discord.User, url: str, summary: str, is_own_request: bool = False
) -> None:
    """Send DM to a specific user."""
    prefix = "Your requested summary" if is_own_request else "Summary"
    await user.send(f"{prefix}: {url}")
    await user.send(f"{summary}")


async def _send_to_multiple_users(
    interaction: discord.Interaction, url: str, summary: str, requester_name: str
) -> None:
    """Send summary to both secondary users and requester."""
    for secondary_username in message_config.secondary_users:
        target_user = discord.utils.get(
            interaction.guild.members, name=secondary_username # type: ignore
        )
        if target_user:
            await target_user.send(f"Summary requested by {requester_name}: {url}")
            await target_user.send(f"{summary}")
            print(f"Sent summary to {secondary_username}")
        else:
            print(f"Could not find user {secondary_username}")

    await _send_dm_to_user(interaction.user, url, summary, is_own_request=True) # type: ignore


async def send_research_to_users(
    interaction: discord.Interaction, topic: str, file_path: str
) -> None:
    """
    Send research PDF to appropriate users.
    Uses MessageConfig to determine who should receive research files.

    Args:
        interaction: Discord interaction object
        topic: The research topic
        file_path: Path to the PDF file
    """
    try:
        if os.path.exists(file_path):
            file = discord.File(file_path, filename=os.path.basename(file_path))
            await interaction.followup.send(
                f"Here's your research on '{topic}':", file=file
            )

            # Send to all secondary users (admins/special users)
            for target_username in message_config.secondary_users:
                target_user = discord.utils.get(
                    interaction.guild.members, name=target_username # type: ignore
                )
                if target_user:
                    await target_user.send(
                        f"Research on '{topic}' requested by {interaction.user.name}:",
                        file=discord.File(
                            file_path, filename=os.path.basename(file_path)
                        ),
                    )
                    print(f"Sent research to {target_username}")
                else:
                    print(f"Could not find user {target_username}")
            await interaction.followup.send(
                "Research completed, check your DMs!", ephemeral=True
            )
        else:
            await interaction.followup.send(
                "Research completed but couldn't find the PDF file.", ephemeral=True
            )
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


class MessageConfig:
    """Configuration class for message routing."""

    def __init__(self):
        self.primary_users = [
            "kazul31303"
        ]  # Users who get exclusive access to their requests
        self.secondary_users = ["kazul3103"]  # Users who receive others' requests
        self.admin_users = ["kazul3103"]  # Users with admin privileges

    def is_primary_user(self, username: str) -> bool:
        return username in self.primary_users

    def is_secondary_user(self, username: str) -> bool:
        return username in self.secondary_users

    def is_admin_user(self, username: str) -> bool:
        return username in self.admin_users


message_config = MessageConfig()
