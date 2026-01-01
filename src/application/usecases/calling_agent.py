from src.utils.youtube import load_youtube_transcript, YouTubeTranscriptPreprocessor
from src.utils.chunking import process_chunking
from src.application.AI.summary.summary_agent import summary_agent
from src.application.AI.research.research_agent import reporter_agent
from src.application.AI.free_chat.chat import free_chat_prompt_to_messages
from src.application.AI.bad_word_detection.bad_word_agent import KLASIFIKASI_BAD_WORD

async def call_agent(agent, param, config={"recursion_limit": 50}):
    events = await agent.ainvoke(
        param,
        config,
    )
    return events


async def youtube_summary(youtube_url: str):
    preprocessor = YouTubeTranscriptPreprocessor()
    docs = load_youtube_transcript(youtube_url)
    print("--------------")
    youtube_content = " ".join(docs.get("transcript", "")).strip()
    print("youtube transcipt: ", youtube_content)
    
    if youtube_content == "no transcript found":
        raise ValueError("No transcipt found from youtube url. - ", youtube_content)

    youtube_content = preprocessor.preprocess(
        youtube_content,
        remove_fillers=True,
        aggressive_filler_removal=True,
        expand_contractions=True,
    )
    youtube_content = process_chunking(
        content=youtube_content, chunk_size=500, chunk_overlap=50
    )
    params = {"contents": [doc.page_content for doc in youtube_content]}
    result = await call_agent(agent=summary_agent, param=params)
    return result


async def research_topic(topic: str):
    param = {"topic": topic}
    result = await call_agent(agent=reporter_agent, param=param)
    return result


async def free_chat(prompt_usr: str, name: str = "", id: str = ""):
    ai_message = free_chat_prompt_to_messages(prompt_usr, name, id)
    return ai_message


async def klasifikasi_bad_word(text_to_check: str):  
    print("ini text yang perlu di kalasifikasi: ", text_to_check)  
    response = KLASIFIKASI_BAD_WORD.invoke({"messages": [
        {"role": "user", "content":text_to_check}]},
                                           context={"level": "basic"})['structured_response']
    print("ini response klasifikasi: ", response)
    return response.is_bad_word