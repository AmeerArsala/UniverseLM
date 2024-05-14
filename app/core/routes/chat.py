from typing import Union, Optional, List, Dict
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, StreamingResponse

from app.lib.chat import AgentChat, AgentChatParams, manifest_chat
from app.lib import users


router = APIRouter()


def retrieve_chat_response(chat: AgentChat, inputs: Dict, stream_response: bool):
    if stream_response:
        return StreamingResponse(
            chat.generate_chat_response_events(inputs, add_to_history=True),
            media_type="text/event-stream",
        )
    else:  # not async
        invocation = chat.invoke_chat(inputs, add_to_history=True)
        response: str = invocation["answer"]

        return response


class ChatParams(BaseModel):
    user_id: int
    message: str
    stream_response: bool


@router.post("/community/{community_id}/chat/{chunk_name}")
async def chat_with_agent(
    community_id: int, chunk_name: str, params: ChatParams
) -> str:
    # manifest the chat from nothing or a cache
    chat: AgentChat = manifest_chat(
        community_id, chunk_name, stream_response=params.stream_response
    )

    agent_chat_params: AgentChatParams = users.make_chat_input(
        user_id=params.user_id, message=params.message
    )
    agent_chat_inputs: Dict = agent_chat_params.dict()

    # Chat response
    print("Generating response...")
    return retrieve_chat_response(chat, agent_chat_inputs, params.stream_response)
