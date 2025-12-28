from .message import (send_summary_to_users, 
                      send_research_to_users, 
                      bot, 
                      handle_bad_words, 
                      handle_ai_chat)
from src.application.usecases.calling_agent import (research_topic, 
                                                    youtube_summary,
                                                    free_chat)
from src.application.services.keep_alive import keep_alive
from markdown_pdf import MarkdownPdf, Section
from dotenv import load_dotenv
import discord
import os

keep_alive()
load_dotenv()

pdf = MarkdownPdf(toc_level=2, optimize=True)

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
  

# @bot.event
# async def on_message(message):
#     # Abaikan pesan dari bot itu sendiri
#     if message.author == bot.user:
#         return
#     print("-----------")
#     print(f"Content dibaca: '{message.content}'")

#     was_bad_word = await handle_bad_words(message)
#     if was_bad_word:
#         return # Berhenti di sini jika pesan sudah dihapus

#     await handle_ai_chat(message)
#     await bot.process_commands(message)
    

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
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=False)


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
