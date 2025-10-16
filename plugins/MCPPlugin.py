"""
MCP (Model Context Protocol) Plugin

This module creates and configures the MCP plugin for email notifications.
It connects to the MCP server running on localhost:8080 and provides
email notification capabilities to the MCPAgent.

Author: MultiAgent-SemanticKernel-Python
"""

import os
from dotenv import load_dotenv
from semantic_kernel.connectors.mcp import MCPSsePlugin
import asyncio

# Load environment variables
load_dotenv("config.env")


async def create_email_mcp_plugin():
    """
    Create and configure the MCP plugin for email notifications.
    
    This function initializes the MCP SSE plugin that connects to the
    email notification server and loads the available tools.
    
    Returns:
        MCPSsePlugin: Configured MCP plugin for email notifications
    """
    # Initialize MCP SSE plugin
    plugin = MCPSsePlugin(
        name="EmailMCP",
        description="Email notification plugin",
        url="http://127.0.0.1:8080/sse",
        load_tools=True,
        load_prompts=False
    )

    # Connect to the MCP server and load tools
    await plugin.connect()
    await plugin.load_tools()

    # Fix deepcopy issue for the plugin
    def _no_deepcopy(self, memo):
        return self
    plugin.__deepcopy__ = _no_deepcopy.__get__(plugin, type(plugin))

    # Debug: List available plugin functions
    print("[DEBUG] Plugin functions ready:")
    for attr in dir(plugin):
        if not attr.startswith("_"):
            if callable(getattr(plugin, attr)):
                print("  -", attr)

    return plugin


