from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_chunking(
    content: str, chunk_size: int = 2000, chunk_overlap: int = 150
):
    """
    Process a YouTube transcript by loading, preprocessing, and chunking it.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents([content])

    return texts
