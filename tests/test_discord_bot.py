import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.interface.discord.main import research, summary, poll
from src.interface.discord.main import chat_ai
import discord

# Path target untuk patching
TARGET = 'src.interface.discord.main'

@pytest.fixture
def mock_interaction():
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    interaction.user.mention = "@tester"
    return interaction


@pytest.mark.asyncio
async def test_on_message_deletes_bad_word():
    from src.interface.discord.main import on_message
    mock_message = AsyncMock()
    mock_message.author = MagicMock()
    mock_message.author.mention = "@user_test"
    mock_message.content = "This is a shit post"
    mock_message.channel.send = AsyncMock()
    mock_message.delete = AsyncMock()

    with patch('src.interface.discord.main.bot') as mock_bot:
        mock_bot.user = MagicMock()
        mock_bot.process_commands = AsyncMock() 
        await on_message(mock_message)

    # Verifikasi
    mock_message.delete.assert_called_once()
    mock_bot.process_commands.assert_called_once_with(mock_message)


@pytest.mark.asyncio
async def test_chat_ai_command(mock_interaction):
    """Menguji command /chat_ai"""
    question = "Tips belajar Python?"
    await chat_ai.callback(mock_interaction, 
                           question=question) # type: ignore
    assert mock_interaction.response.send_message.call_count == 2

@pytest.mark.asyncio
async def test_research_command_error_handling(mock_interaction):
    """Menguji error handling pada command /research"""
    
    with patch(f'{TARGET}.research_topic', side_effect=Exception("API Down")), \
         patch(f'{TARGET}.pdf'), \
         patch('os.path.exists', return_value=False):
        await research.callback(mock_interaction,
                                topic="AI",  # type: ignore
                                pdf_name="test_file")
        
        mock_interaction.followup.send.assert_called_with(
            "An error occurred: API Down", ephemeral=True
        )

@pytest.mark.asyncio
async def test_summary_command_success(mock_interaction):
    """Menguji command /summary"""
    url = "https://youtube.com/watch?v=123"
    mock_result = {"summary": "Ini ringkasan."}
    
    with patch(f'{TARGET}.youtube_summary', return_value=mock_result), \
         patch(f'{TARGET}.send_summary_to_users', new_callable=AsyncMock):
        # PERBAIKAN: Gunakan .callback
        await summary.callback(mock_interaction, 
                               url=url) # type: ignore
        mock_interaction.followup.send.assert_any_call(
            f"{mock_result['summary']}", ephemeral=False
        )


@pytest.mark.asyncio
async def test_poll_command_logic(mock_interaction):
    """Menguji command /poll"""
    mock_poll_msg = AsyncMock()
    mock_interaction.original_response.return_value = mock_poll_msg
    await poll.callback(mock_interaction, 
                        question="Pertanyaan?") # type: ignore
    
    mock_poll_msg.add_reaction.assert_any_call("👍")