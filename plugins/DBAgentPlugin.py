"""
Database Agent Plugin

This plugin provides database operations for task management including
adding, listing, updating, and deleting tasks. It's used by the DBAgent
to handle all task-related database operations.

Author: MultiAgent-SemanticKernel-Python
"""

from semantic_kernel.functions import kernel_function
from db import execute_query
from typing import Optional


class DBAgentPlugin:
    """
    Plugin for database operations related to task management.
    
    This plugin provides kernel functions that can be called by the DBAgent
    to perform CRUD operations on tasks in the database.
    """

    @kernel_function(name="add_task", description="Add a new task to the database.")
    def add_task(self, employee: str, email: str, description: str, due_date: Optional[str] = None) -> str:
        """
        Add a new task to the database.
        
        Args:
            employee: Name of the employee assigned to the task
            email: Email address for sending notifications
            description: Description of the task
            due_date: Optional due date for the task
            
        Returns:
            str: Success message or error description
        """
        # Validate email is provided for notifications
        if not email:
            return f"Email for {employee} is missing. Please provide an email address to send the task notification."
        
        # Insert task into database
        execute_query(
            "INSERT INTO tasks (employee, description, due_date) VALUES (?, ?, ?)",
            (employee, description, due_date)
        )
        
        return f"Task '{description}' has been successfully added for {employee}. Please handoff to MCPAgent to send email notification to {email}."

    @kernel_function(name="list_pending_tasks", description="List all pending tasks for a person.")
    def list_pending_tasks(self, employee: str) -> str:
        """
        List all pending tasks for a specific employee.
        
        Args:
            employee: Name of the employee
            
        Returns:
            str: Formatted list of pending tasks or message if none found
        """
        rows = execute_query(
            "SELECT id, description, due_date FROM tasks WHERE employee = ? AND status = 'pending'",
            (employee,),
            fetch=True
        )
        
        if not rows:
            return f"No pending tasks for {employee}."
            
        # Format task list with ID, description, and due date
        return "\n".join([f"[{id}] {desc} (Due: {due or 'N/A'})" for id, desc, due in rows])

    @kernel_function(name="mark_task_done", description="Mark a task as completed by ID.")
    def mark_task_done(self, email: str, id: int) -> str:
        """
        Mark a task as completed by its ID.
        
        Args:
            email: Email address for sending completion notification
            id: Task ID to mark as completed
            
        Returns:
            str: Confirmation message
        """
        execute_query("UPDATE tasks SET status = 'done' WHERE id = ?", (id,))
        return f"Task {id} marked as completed."

    @kernel_function(name="delete_task", description="Delete a task by ID.")
    def delete_task(self, id: int) -> str:
        """
        Delete a task by its ID.
        
        Args:
            id: Task ID to delete
            
        Returns:
            str: Confirmation message
        """
        execute_query("DELETE FROM tasks WHERE id = ?", (id,))
        return f"Task {id} deleted."
