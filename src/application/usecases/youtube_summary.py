from src.utils.youtube import load_youtube_transcript, YouTubeTranscriptPreprocessor
from src.utils.chunking import process_chunking
from src.application.AI.summary.summary_agent import summary_agent
from .calling_agent import call_agent


async def youtube_summary(youtube_url: str):
    preprocessor = YouTubeTranscriptPreprocessor()
    param = {
        "youtube_url": youtube_url
    }
    docs = load_youtube_transcript(youtube_url)
    youtube_content = " ".join(docs.get('transcript', '')).strip()
    
    youtube_content = preprocessor.preprocess(
        youtube_content,
        remove_fillers=True,
        aggressive_filler_removal=True,
        expand_contractions=True,
    )
    youtube_content = process_chunking(content=youtube_content, chunk_size=500, chunk_overlap=50)
    params = {"contents": [doc.page_content for doc in youtube_content]}
    result = await call_agent(agent=summary_agent, param=params)
    return result
    