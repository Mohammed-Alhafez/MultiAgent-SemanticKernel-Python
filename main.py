"""
Multi-Agent Task Management System

This module serves as the main entry point for a multi-agent system built with
Microsoft Semantic Kernel. The system consists of specialized agents that handle
task management, company information queries, and email notifications through
intelligent handoff orchestration.

The system includes:
- TriageAgent: Routes requests to appropriate specialized agents
- DBAgent: Manages task creation, assignment, and completion
- InformativeAgent: Provides company policies and HR information
- MCPAgent: Handles email notifications for task updates

Author: MultiAgent-SemanticKernel-Python
"""

from semantic_kernel.agents.runtime import InProcessRuntime
import asyncio
from db import init_db, init_chat_history_table
from Agents.agent_set import triage_agent, db_agent, informative_agent, init_mcp_agent
from orchestrator import build_handoff_orchestration


async def main():
    """
    Main entry point for the multi-agent task management system.
    
    Initializes the database, starts the runtime, creates all agents,
    and begins the interactive chat loop for user requests.
    """
    # Initialize database and chat history table
    init_db()
    init_chat_history_table()

    # Start the Semantic Kernel runtime
    runtime = InProcessRuntime()
    runtime.start()

    # Initialize MCP agent for email notifications
    mcp_agent = await init_mcp_agent()

    # Build the handoff orchestration with all agents
    handoff_orchestration = build_handoff_orchestration(
        triage_agent, db_agent, informative_agent, mcp_agent
    )

    print("Multi-Agent Task Management System")
    print("=" * 40)
    print("Enter your request (type 'exit' to quit):")
    
    # Main interaction loop
    while True:
        user_input = input("\nUser > ")
        
        # Handle exit command
        if user_input.lower().strip() == "exit":
            print("Goodbye! Thank you for using the system.")
            break
            
        # Skip empty inputs
        if not user_input.strip():
            continue

        try:
            # Process user request through the orchestration system
            result = await handoff_orchestration.invoke(
                task=user_input,
                runtime=runtime,
            )
            final_output = await result.get()
            print(f"\n[Final Output] {final_output}")
            
        except Exception as e:
            print(f"Error processing request: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
