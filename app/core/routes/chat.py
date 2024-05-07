from typing import Union, Optional, List, Dict
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, StreamingResponse

from app.lib.chat import AgentChat, manifest_chat


router = APIRouter()


def retrieve_chat_response(chat: AgentChat, message: str, stream_response: bool):
    if stream_response:
        return StreamingResponse(
            chat.generate_chat_response_events(message, add_to_history=True),
            media_type="text/event-stream",
        )
    else:  # not async
        invocation = chat.invoke_chat({"question": message}, add_to_history=True)
        response: str = invocation["answer"]

        return response


class ChatParams(BaseModel):
    message: str
    stream_response: bool


@router.post("/agents/{chunk_name}")
async def chat_with_agent(chunk_name: str, params: ChatParams) -> str:
    # manifest the chat from nothing or a cache
    chat: AgentChat = manifest_chat(chunk_name)

    chat: PapersChat = manifest_chat(
        chat_id,
        paper_ids=params.paper_ids,
        chatbot_generator=lambda: manifest_rag_chatbot(
            unique_doc_id=unique_doc_id,
            session=kdbai_session,
            text_chunks=flattened_text_chunks,
            stream_response=params.stream_response,
        ),
    )

    # RAG the docs
    print("Generating response...")
    return retrieve_chat_response(chat, params.message, params.stream_response)
