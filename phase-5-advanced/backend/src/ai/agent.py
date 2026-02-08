# src/ai/agent.py
import os
from openai import OpenAI
from src.mcp_tools.task_tools import (
    add_task, list_tasks, complete_task, 
    delete_task, update_task
)
import json

# Hardcoded API credentials (permanent solution)
OPENAI_API_KEY = "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"
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

# Initialize OpenAI client with OpenRouter
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

# Define tools for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Get all tasks. Status can be: all, pending, completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

async def run_agent(user_id: int, message: str, conversation_history: list):
    """Run AI agent with MCP tools"""
    
    # Build messages
    messages = [
        {"role": "system", "content": "You are a helpful todo assistant. Help users manage their tasks using the available tools."}
    ]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})
    
    # Call OpenAI
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Check if tool was called
    if assistant_message.tool_calls:
        # Execute tool
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Call appropriate tool
            if function_name == "add_task":
                result = await add_task(**function_args)
            elif function_name == "list_tasks":
                result = await list_tasks(**function_args)
            elif function_name == "complete_task":
                result = await complete_task(**function_args)
            elif function_name == "delete_task":
                result = await delete_task(**function_args)
            elif function_name == "update_task":
                result = await update_task(**function_args)
            
            # Add tool result to messages
            messages.append(assistant_message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
            
            # Get final response
            final_response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=messages
            )
            
            return final_response.choices[0].message.content
    
    return assistant_message.content