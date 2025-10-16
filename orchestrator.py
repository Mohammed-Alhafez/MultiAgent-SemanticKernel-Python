"""
Orchestration Module for Multi-Agent System

This module handles the coordination and handoff logic between different agents
in the multi-agent task management system. It defines how agents transfer control
to each other based on the type of user request and manages the streaming
responses and chat history.

Author: MultiAgent-SemanticKernel-Python
"""

from semantic_kernel.agents import OrchestrationHandoffs, HandoffOrchestration
from semantic_kernel.contents import (
    AuthorRole, 
    ChatMessageContent, 
    FunctionCallContent, 
    FunctionResultContent, 
    StreamingChatMessageContent
)
from db import store_chat_message
import uuid

# Global variables for session management
is_new_message = True
session_id = str(uuid.uuid4())


def streaming_agent_response_callback(message: StreamingChatMessageContent, is_final: bool) -> None:
    """
    Callback function for handling streaming agent responses.
    
    This function processes streaming messages from agents, displays them to the user,
    and stores them in the chat history database.
    
    Args:
        message: The streaming message content from an agent
        is_final: Whether this is the final message in the stream
    """
    global is_new_message
    
    # Display agent name for new messages
    if is_new_message:
        print(f"{message.name}> ", end="", flush=True)
        is_new_message = False

    # Display and store message content
    if message.content:
        print(message.content, end="", flush=True)
        store_chat_message(
            session_id=session_id,
            role="agent",
            agent_name=message.name,
            content=message.content
        )

    # Handle function calls and results
    for item in message.items:
        if isinstance(item, FunctionCallContent):
            print(f"\n[DEBUG] Tool call received from agent: {item.name} with args {item.arguments}")
            print(f"\nCalling '{item.name}' with arguments '{item.arguments}'", end="", flush=True)
            store_chat_message(session_id, "function", item.name, f"Called with: {item.arguments}")
            
        if isinstance(item, FunctionResultContent):
            print(f"\nResult from '{item.name}' is '{item.result}'", end="", flush=True)
            store_chat_message(session_id, "function", item.name, f"Result: {item.result}")

    # Reset for next message when stream is complete
    if is_final:
        print()
        is_new_message = True


async def human_response_function(prompt: str = "") -> ChatMessageContent:
    """
    Function to handle human user input during agent interactions.
    
    Args:
        prompt: Optional prompt to display to the user
        
    Returns:
        ChatMessageContent: The user's input formatted as a chat message
    """
    user_input = input(f"User > {prompt}")
    store_chat_message(session_id=session_id, role="user", agent_name=None, content=user_input)
    return ChatMessageContent(role=AuthorRole.USER, content=user_input)


def build_handoff_orchestration(triage_agent, db_agent, informative_agent, mcp_agent):
    """
    Builds the handoff orchestration system that defines how agents transfer control.
    
    This function creates the orchestration rules that determine when and how
    agents hand off control to each other based on the type of user request.
    
    Args:
        triage_agent: The main routing agent
        db_agent: Agent responsible for task management
        informative_agent: Agent for company information queries
        mcp_agent: Agent for email notifications
        
    Returns:
        HandoffOrchestration: Configured orchestration system
    """
    # Define handoff rules between agents
    handoffs = (
        OrchestrationHandoffs()
        # Triage agent can hand off to specialized agents
        .add_many(
            source_agent=triage_agent.name,
            target_agents={
                db_agent.name: "Transfer to this agent if the issue is related to tasks or assignments.",
                informative_agent.name: "Transfer to this agent if the issue is related to company policies or information.",
                mcp_agent.name: "Transfer to this agent if a task was added or completed and a notification must be sent."
            },
        )
        # DB agent can return to triage or send notifications
        .add(
            source_agent=db_agent.name,
            target_agent=triage_agent.name,
            description="Transfer if not task-related.",
        )
        .add(
            source_agent=db_agent.name,
            target_agent=mcp_agent.name,
            description="Transfer when a task is added or completed and email must be sent.",
        )
        # Informative agent returns to triage for non-information requests
        .add(
            source_agent=informative_agent.name,
            target_agent=triage_agent.name,
            description="Transfer if not information-related.",
        )
        # MCP agent returns to triage after sending notifications
        .add(
            source_agent=mcp_agent.name,
            target_agent=triage_agent.name,
            description="Transfer after notification has been sent.",
        )
    )

    return HandoffOrchestration(
        members=[triage_agent, db_agent, informative_agent, mcp_agent],
        handoffs=handoffs,
        streaming_agent_response_callback=streaming_agent_response_callback,
        human_response_function=human_response_function,
    )
