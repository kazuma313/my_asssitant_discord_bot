from .message import send_summary_to_users, send_research_to_users
from src.application.usecases.research_topic import research_topic
from src.application.usecases.youtube_summary import youtube_summary
# from src.application.services.keep_alive import keep_alive
from markdown_pdf import MarkdownPdf, Section
from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

# keep_alive()
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
    # await member.send(f"Welcome to the server {member.name}")
    await member.channel.send(f"Welcome to the server {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"bad word detected from - {message.author.mention}")

    await bot.process_commands(message)


# Command: Simple greeting
@bot.tree.command(
    name="chat_ai", description="chat ai about tips and trick of tehcnology"
)
async def chat_ai(interaction: discord.Interaction, question: str):
    await interaction.response.send_message(f"Processing your question: {question}", ephemeral=True)
    await interaction.response.send_message(
        f"Hello {interaction.user.mention}! How can I assist you today?"
    )


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
