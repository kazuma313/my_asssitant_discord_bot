from .message import send_summary_to_users, send_research_to_users
from src.application.usecases.calling_agent import (research_topic, 
                                                    youtube_summary,
                                                    free_chat,
                                                    klasifikasi_bad_word)
from src.application.services.keep_alive import keep_alive
from markdown_pdf import MarkdownPdf, Section
from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

keep_alive()
load_dotenv()

secret_role = "explorer"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

pdf = MarkdownPdf(toc_level=2, optimize=True)
bot = commands.Bot(command_prefix="/", description=description, intents=intents)


@bot.event
async def on_ready():
    print("We are ready to go")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_member_join(member):
    await member.channel.send(f"Welcome to the server {member.name}")
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print("-----------")
    print(f"Content dibaca: '{message.content}'") 

    # 1. Filter Bad Word dengan tambahan pengecekan
    try:
        print("Sedang mengecek bad word...")
        # Tambahkan timeout jika fungsi AI memakan waktu terlalu lama
        is_bad_word = await klasifikasi_bad_word(text_to_check=message.content)
        print(f"Hasil klasifikasi: '{is_bad_word}'")
    except Exception as e:
        print(f"Error di fungsi klasifikasi_bad_word: {e}")
        is_bad_word = "no" # Default ke 'no' jika error agar bot tidak stuck

    if str(is_bad_word).lower() == "yes":
        try:
            await message.delete()
            await message.channel.send(f"Please mind your manner!!! - {message.author.mention}")
            print("Pesan buruk dihapus.")
        except Exception as e:
            print(f"Gagal menghapus/mengirim pesan peringatan: {e}")
        return 

    # 2. Fitur Chat AI (Tag/Mention)
    if bot.user.mentioned_in(message): # type: ignore
        print("Bot di-mention, memproses jawaban...")
        clean_content = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip() # type: ignore
        
        if clean_content == "":
            await message.channel.send(f"Halo {message.author.mention}! Ada yang bisa saya bantu?")
        else:
            loading_msg = await message.reply("⏳ Memproses pertanyaanmu...")
            try:
                ai_response = await free_chat(clean_content)
                content_to_send = ai_response.content if hasattr(ai_response, 'content') else ai_response
                await message.reply(str(content_to_send))
                await loading_msg.delete() 
            except Exception as e:
                print(f"Error AI: {e}")
                await loading_msg.edit(content="Maaf, terjadi kendala teknis.")

    await bot.process_commands(message)
    

@bot.tree.command(
    name="chat_ai", description="chat ai about tips and trick of tehcnology"
)
async def chat_ai(interaction: discord.Interaction, question: str):
    try:
        await interaction.response.send_message(f"Processing your question: {question}", ephemeral=True)
        ai_message = await free_chat(question)
        await interaction.followup.send(str(ai_message.content))
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


@bot.tree.command(name="research", description="research a topic")
async def research(interaction: discord.Interaction, topic: str, pdf_name: str):
    try:
        await interaction.response.defer(ephemeral=False)
        result_research = await research_topic(topic)
        pdf.add_section(Section(result_research))
        pdf.meta["title"] = topic
        pdf.meta["author"] = "Kurnia Zulda"
        pdf.save(f"{pdf_name}.pdf")

        file_path = f"{pdf_name}.pdf"
        await send_research_to_users(interaction, topic, file_path)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        file_path = f"{pdf_name}.pdf"
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file after error: {file_path}")
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


@bot.tree.command(name="summary", description="summary from youtube url")
async def summary(interaction: discord.Interaction, url: str):
    try:
        await interaction.response.defer(ephemeral=False)
        result = await youtube_summary(url)
        await interaction.followup.send(
            f"summary of the youtube video url: {url}", ephemeral=False
        )
        await interaction.followup.send(f"{result['summary']}", ephemeral=False)
        await send_summary_to_users(interaction, url, result["summary"])
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


@bot.tree.command(
    name="poll",
    description="Creates a poll with the given question and adds thumbs up/down reactions",
)
async def poll(
    interaction: discord.Interaction,
    question: str,
):
    embed = discord.Embed(title="ISI POLL!!!!", description=question)
    await interaction.response.send_message(embed=embed)
    poll_message = await interaction.original_response()
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
