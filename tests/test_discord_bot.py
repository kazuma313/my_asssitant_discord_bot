import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from src.interface.discord.main import research, summary, poll, chat_ai

# Path target patching
TARGET = 'src.interface.discord.main'


@pytest.fixture
def mock_message():
    """Fixture untuk mensimulasikan pesan masuk"""
    message = AsyncMock(spec=discord.Message)
    message.content = ""
    message.author = MagicMock(spec=discord.Member)
    message.author.bot = False
    message.author.mention = "@tester"
    message.channel = AsyncMock()
    message.reply = AsyncMock()
    message.delete = AsyncMock()
    return message

@pytest.mark.asyncio
async def test_on_message_deletes_bad_word(mock_message, mock_bot_user):
    """Menguji on_message ketika mengandung kata kasar"""
    from src.interface.discord.main import on_message
    
    mock_message.content = "anjing" # Contoh kata kasar
    # Pastikan bot user ID tidak sama dengan author ID agar tidak diabaikan
    mock_bot_user.user.id = 999 
    mock_message.author.id = 111

    # Patch handle_bad_words agar mengembalikan True (terdeteksi bad word)
    with patch('src.interface.discord.main.handle_bad_words', new_callable=AsyncMock) as mock_handle:
        mock_handle.return_value = True
        
        await on_message(mock_message)
        
        # Verifikasi: handle_bad_words dipanggil
        mock_handle.assert_called_once_with(mock_message)
        # on_message harus berhenti (return) dan tidak lanjut ke handle_ai_chat
        with patch('src.interface.discord.main.handle_ai_chat', new_callable=AsyncMock) as mock_ai:
            await on_message(mock_message)
            mock_ai.assert_not_called()

@pytest.mark.asyncio
async def test_on_message_allows_good_word_and_calls_ai(mock_message, mock_bot_user):
    """Menguji on_message ketika pesan bersih dan lanjut ke AI chat"""
    from src.interface.discord.main import on_message
    
    mock_message.content = "Halo bot, apa kabar?"
    mock_bot_user.user.id = 999
    mock_message.author.id = 111

    with patch('src.interface.discord.main.handle_bad_words', new_callable=AsyncMock) as mock_bad, \
         patch('src.interface.discord.main.handle_ai_chat', new_callable=AsyncMock) as mock_ai, \
         patch('src.interface.discord.main.bot.process_commands', new_callable=AsyncMock) as mock_cmd:
        
        mock_bad.return_value = False
        
        await on_message(mock_message)
        
        # Verifikasi alur:
        mock_bad.assert_called_once() # Cek bad word dulu
        mock_ai.assert_called_once_with(mock_message) # Lanjut ke AI
        mock_cmd.assert_called_once_with(mock_message) # Lanjut ke command processing

@pytest.mark.asyncio
async def test_handle_ai_chat_mention(mock_message, mock_bot_user):
    """Menguji fungsi handle_ai_chat saat bot di-mention"""
    # Import lokal untuk menghindari circular import
    from src.interface.discord.message import handle_ai_chat, bot
    
    # 1. Setup Mocking
    bot_id = 999
    mock_bot_user.user.id = bot_id
    
    # Pastikan bot.user.mentioned_in(message) mengembalikan True
    bot.user.mentioned_in.return_value = True
    
    # Isi pesan yang mensimulasikan mention
    mock_message.content = f"<@{bot_id}> apa itu python?"
    
    # Mock respons dari AI
    mock_ai_res = MagicMock()
    mock_ai_res.content = "Python adalah bahasa pemrograman."

    with patch('src.interface.discord.message.free_chat', new_callable=AsyncMock) as mock_free:
        mock_free.return_value = mock_ai_res
        
        # 2. Eksekusi
        await handle_ai_chat(mock_message)
        
        # 3. Verifikasi
        # Verifikasi loading message dikirim (menggunakan assert_any_call)
        mock_message.reply.assert_any_call("⏳ Memproses pertanyaanmu...")
        
        # Verifikasi jawaban AI dikirim
        mock_message.reply.assert_any_call("Python adalah bahasa pemrograman.")
        
        # Verifikasi pesan loading dihapus setelah selesai
        # (Di kode Anda ada loading_msg.delete(), kita perlu pastikan itu terpanggil)
        assert mock_message.reply.return_value.delete.called
        

@pytest.fixture
def mock_interaction():
    interaction = AsyncMock(spec=discord.Interaction)
    # Mocking response
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    
    # Mock User
    mock_user = MagicMock(spec=discord.Member)
    mock_user.name = "tester"
    mock_user.mention = "@tester"
    interaction.user = mock_user
    
    # Mock Guild untuk fungsi _send_to_multiple_users
    interaction.guild = MagicMock(spec=discord.Guild)
    interaction.guild.members = []

    # Mocking original_response untuk command /poll
    interaction.original_response = AsyncMock()
    return interaction

@pytest.fixture(autouse=True)
def mock_bot_user():
    # Ini untuk mencegah error 'NoneType' object has no attribute 'mentioned_in'
    # Kita patch 'bot' yang ada di module main dan message
    with patch('src.interface.discord.message.bot') as mock_bot:
        mock_bot.user = MagicMock(spec=discord.ClientUser)
        mock_bot.user.id = 12345
        mock_bot.user.mentioned_in.return_value = False
        yield mock_bot

@pytest.mark.asyncio
async def test_chat_ai_command_success(mock_interaction):
    """Menguji command /chat_ai saat berhasil"""
    question = "Tips belajar Python?"
    
    # Mock return value dari free_chat (karena di code Anda memanggil .content)
    mock_ai_response = MagicMock()
    mock_ai_response.content = "Belajar dasar-dasar sintaks."

    with patch(f'{TARGET}.free_chat', new_callable=AsyncMock) as mock_free_chat:
        mock_free_chat.return_value = mock_ai_response
        
        # Eksekusi callback
        await chat_ai.callback(mock_interaction, question=question)

        # Verifikasi:
        mock_interaction.response.send_message.assert_called_once_with(
            f"Processing your question: {question}", ephemeral=True
        )
        mock_interaction.followup.send.assert_called_once_with("Belajar dasar-dasar sintaks.")

@pytest.mark.asyncio
async def test_research_command_success(mock_interaction):
    """Menguji command /research saat berhasil"""
    topic = "AI"
    pdf_name = "test_res"
    
    with patch(f'{TARGET}.research_topic', new_callable=AsyncMock) as mock_res, \
         patch(f'{TARGET}.pdf') as mock_pdf, \
         patch(f'{TARGET}.send_research_to_users', new_callable=AsyncMock) as mock_send, \
         patch('os.path.exists', return_value=True), \
         patch('os.remove') as mock_remove:
        
        mock_res.return_value = "Hasil riset mendalam."
        
        await research.callback(mock_interaction, topic=topic, pdf_name=pdf_name) # type: ignore

        # Verifikasi
        mock_interaction.response.defer.assert_called_once_with(ephemeral=False)
        mock_pdf.add_section.assert_called()
        mock_pdf.save.assert_called_with(f"{pdf_name}.pdf")
        mock_send.assert_called_once()

@pytest.mark.asyncio
async def test_summary_command_success(mock_interaction):
    """Menguji command /summary"""
    url = "https://youtube.com/watch?v=123"
    mock_result = {"summary": "Ini ringkasan video."}
    
    # Penting: Mock send_summary_to_users karena fungsi ini mengakses message_config
    with patch(f'{TARGET}.youtube_summary', new_callable=AsyncMock) as mock_sum, \
         patch(f'{TARGET}.send_summary_to_users', new_callable=AsyncMock) as mock_send:
        
        mock_sum.return_value = mock_result
        
        await summary.callback(mock_interaction, url=url) # type: ignore

        # Verifikasi
        mock_interaction.response.defer.assert_called_once_with(ephemeral=False)
        # Cek apakah salah satu pemanggilan followup.send berisi summary
        mock_interaction.followup.send.assert_any_call("Ini ringkasan video.", ephemeral=False)
        mock_send.assert_called_once()

@pytest.mark.asyncio
async def test_poll_command_logic(mock_interaction):
    """Menguji command /poll"""
    mock_poll_msg = AsyncMock()
    mock_interaction.original_response.return_value = mock_poll_msg
    
    question = "Apakah hari ini cerah?"
    await poll.callback(mock_interaction, question=question) # type: ignore
    
    # Verifikasi embed
    assert mock_interaction.response.send_message.called
    args, kwargs = mock_interaction.response.send_message.call_args
    assert isinstance(kwargs['embed'], discord.Embed)
    
    # Verifikasi reaksi
    mock_poll_msg.add_reaction.assert_any_call("👍")
    mock_poll_msg.add_reaction.assert_any_call("👎")