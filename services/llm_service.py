
from langchain_ollama import ChatOllama


MODEL_NAME = "llama3.1"


def get_llm():
    """
    Returns a configured Ollama chat model.
    """

    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=0
    )

    return llm
