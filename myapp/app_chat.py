
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from typing import List
# from langchain.memory import SQLiteChatMessageHistory
# from django.core.exceptions import ObjectDoesNotExist
from fastapi import FastAPI, HTTPException, Depends
# from models import user_table
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate


from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.embeddings import HuggingFaceEmbeddings
import pickle
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq


# Wikipedia Search

llm = ChatGroq(model_name="llama3-8b-8192",
               api_key="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")  # , temperature=0)

wikipedia = WikipediaAPIWrapper()
wikipedia_tool = Tool.from_function(
    name="Wikipedia Search",
    func=wikipedia.run,
    description="Use this tool for general autism-related knowledge and definitions."
)

# ArXiv Research
arxiv = ArxivAPIWrapper()
arxiv_tool = Tool.from_function(
    name="ArXiv Research",
    func=arxiv.run,
    description="Use this tool to find the latest autism research studies."
)

# DuckDuckGoSearchRun
search = DuckDuckGoSearchRun(name="Search")  #

# ✅ Load embedding model
# embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
#
#
#
# def load_embeddings(faiss_db_path="faiss_index"):
#     return FAISS.load_local(faiss_db_path, embedding_model, allow_dangerous_deserialization=True)
#
#
# def query_rag(user_query):
#     """Retrieve relevant autism data for chatbot response."""
#     vector_db = load_embeddings()
#     relevant_chunks = vector_db.similarity_search(user_query, k=3)
#     context = "\n".join([chunk.page_content for chunk in relevant_chunks])
#
#     rag_prompt = f"""
#     Use the following autism data to answer the question.
#     If the answer isn't in the retrieved text, say "I couldn't find a reliable answer."
#
#     ### Autism Data:
#     {context}
#
#     ### Question:
#     {user_query}
#     """
#     return llm.invoke(rag_prompt).content
#
#
# rag_tool = Tool.from_function(
#     name="Clinical Data RAG",
#     func=query_rag,
#     description="Retrieve scientific autism data."
# )

tools = {"Wikipedia": wikipedia_tool, "Arxiv": arxiv_tool, "Search": search}#, "RAG": rag_tool}


# ✅ Define Chat State Model
class ChatState(BaseModel):
    message: str
    llm_response: str = ""


# ✅ Define Chatbot Prompt
CHATBOT_PROMPT = """
You are an AI assistant specializing in autism-related topics.
Reply naturally without repeating introductions.
Use Wikipedia, Arxiv, or Search when needed.
Summarize tool results instead of dumping raw data.

History: {history}
User: {input}
"""

history = []

# ✅ LangGraph Setup
graph = StateGraph(ChatState)


def get_llm_response(state: ChatState) -> dict:
    """Generate response from LLM."""
    chat_history = history[-10:] if history else []
    formatted_history = "\n".join(chat_history)

    prompt = ChatPromptTemplate.from_template(CHATBOT_PROMPT)
    final_prompt = prompt.format(history=formatted_history, input=state.message)

    response = llm.invoke(final_prompt).content
    history.append(f"User: {state.message}")
    history.append(f"AI: {response}")

    return {"llm_response": response}


def check_tools(state: ChatState) -> dict:
    """Check if a tool is needed for the query."""
    if state.llm_response.strip() != "I don't have enough information":
        return state.model_dump()

    tool_prompt = f"""
    # You are a friendly, helpful chatbot specialized in autism information. Your primary goal is to provide accurate, compassionate information about autism spectrum disorder.

    # When responding to queries, follow these guidelines:

    # TOOLS FOR AUTISM-SPECIFIC INFORMATION:
    # 1. wikipedia: Use for general knowledge, definitions, explanations of autism concepts, history of autism research, notable figures in autism advocacy, or broad overview information.

    # 2. arxiv: Use for academic research, scientific papers, recent studies, experimental findings, or technical information about autism.

    # 3. duckduckgo_search: Use for current information, news, blog posts, personal accounts, community resources, service providers, or general autism-related queries.

    # 4. none: Use when the query is conversational, a follow-up, or can be answered with general knowledge about autism without requiring external lookups.

    Return only the tool name.
    Query: {state.message}
    Response:
    """
    tool_response = llm.invoke(tool_prompt).content.lower().strip()

    selected_tool = None
    if "wikipedia" in tool_response:
        selected_tool = "Wikipedia"
    elif "arxiv" in tool_response:
        selected_tool = "Arxiv"
    elif "search" in tool_response:
        selected_tool = "Search"
    # elif "rag" in tool_response:
    #     selected_tool = "RAG"

    if not selected_tool:
        return state.model_dump()

    tool_result = tools[selected_tool].func(state.message)

    summary_prompt = f"""
    Summarize this in **3 sentences max**.

    {tool_result}
    """
    summarized_response = llm.invoke(summary_prompt).content

    history.append(f"AI (Tool-Assisted): {summarized_response}")
    return {"llm_response": summarized_response}


# ✅ Add Nodes to LangGraph
graph.add_node("get_llm_response", get_llm_response)
graph.add_node("check_tools", check_tools)

graph.add_edge(START, "get_llm_response")
graph.add_edge("get_llm_response", "check_tools")
graph.add_edge("check_tools", END)

executor = graph.compile()