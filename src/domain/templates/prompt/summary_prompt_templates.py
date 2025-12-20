from langchain_core.prompts import ChatPromptTemplate

map_systems = """
You are an expert in summarizing texts, especially in the context of YouTube video transcripts. 
Your task is to create a concise summary of the provided text, focusing on the key points and main topics discussed.

{context}

the summary must be the key points of the text.
If found different topics, summarize each topic separately.
maximum 200 words.
the result of the summary must be in Indonesian language.
think carefully before you write the summary and make sure you get the important points of information.
"""

reduce_template = """
The following is a set of summaries:

{docs}

Take these and distill it into a final, consolidated summary of the main themes.
make sure the summary output on markdown format.
seperate each topic with different heading.
the summary must only maximum 250 words, so make sure you just get the important points of information.
the summary must be in Indonesian language.
think carefully before you write the summary and make sure you get the important points of information.
"""

map_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", map_systems),
    ]
)

reduce_prompt = ChatPromptTemplate([("human", reduce_template)])
