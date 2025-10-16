"""
MCP (Model Context Protocol) Server for Email Notifications

This module implements a FastMCP server that provides email notification
functionality for the multi-agent system. It handles sending task-related
notifications via Gmail SMTP.

Author: MultiAgent-SemanticKernel-Python
"""

from fastmcp import FastMCP
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config.env")

# Initialize the MCP server
mcp = FastMCP("EmailMCP", instructions="Send task notifications via Gmail")


@mcp.tool(name="send_task_notification")
def send_task_notification(recipient_email: str, subject: str, body: str) -> str:
    """
    Send email notification for task-related updates.
    
    This function sends email notifications when tasks are created, updated,
    or completed. It uses Gmail SMTP with app-specific passwords for authentication.
    
    Args:
        recipient_email: Email address of the recipient
        subject: Subject line of the email
        body: Body content of the email
        
    Returns:
        str: Success message or error description
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Get credentials from environment variables
        sender_email = os.getenv("SENDER_EMAIL")
        app_password = os.getenv("APP_PASSWORD")
        
        # Validate credentials
        if not sender_email or not app_password:
            return "Error: Email credentials not configured. Please check SENDER_EMAIL and APP_PASSWORD in config.env"

        # Create email message
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        # Send email via Gmail SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender_email, app_password)
            server.send_message(msg)

        return f"Notification sent successfully to {recipient_email}"
        
    except Exception as e:
        # Print detailed error information for debugging
        import traceback
        traceback.print_exc()
        return f"Failed to send notification: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server on localhost
    mcp.run("sse", host="127.0.0.1", port=8080)  
