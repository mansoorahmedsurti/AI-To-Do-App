"""Agent Logic for AI-Powered Todo Chatbot"""

import asyncio
from typing import Dict, Any, Optional
import cohere
import os
import json
from datetime import datetime
import uuid
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.conversation import Conversation, Message
from app.models.user import User
from app.models.todo import Todo  # Import Todo model to perform operations


class TodoAgent:
    def __init__(self):
        # Initialize Cohere client
        self.co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

        # System prompt for the agent
        self.system_prompt = """
        You are a helpful assistant that manages to-do lists.
        You can help users add, list, complete, delete, and update tasks using the available functions.
        Always confirm actions with the user after performing them.
        If a user asks about tasks, use the list_tasks function.
        If a user wants to add a task, use the add_task function.
        If a user wants to complete a task, use the complete_task function.
        If a user wants to delete a task, use the delete_task function.
        If a user wants to update a task, use the update_task function.
        Be conversational and helpful in your responses.
        """

    def process_chat_request(self, user_input: str, user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a chat request and return a response

        Args:
            user_input: The user's message
            user_id: The ID of the authenticated user
            conversation_id: Optional conversation ID (creates new if None)

        Returns:
            Dictionary with response and conversation info
        """
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Load conversation history from database
        conversation, messages = self._load_conversation_history(user_uuid, conversation_id)

        # Format the conversation for Cohere
        chat_history = []
        for msg in messages:
            role = "USER" if msg.role == "user" else "CHATBOT"
            chat_history.append({"role": role, "message": msg.content})

        # Add the current user input
        current_chat_message = user_input

        try:
            # Call Cohere API
            response = self.co.chat(
                message=current_chat_message,
                chat_history=chat_history,
                preamble=self.system_prompt,
                connectors=[{"id": "web-search"}],  # Optional: enable web search
                model="command-r-plus",  # Using a capable Cohere model
            )

            # Extract the response
            final_response_content = response.text

            # Save the new messages to the database
            self._save_messages_to_db(conversation.id, "user", user_input)
            self._save_messages_to_db(conversation.id, "assistant", final_response_content)

            return {
                "conversation_id": str(conversation.id),
                "response": final_response_content,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success"
            }

        except Exception as e:
            # Log the error in a real application
            print(f"Error calling Cohere API: {e}")

            # Save the user message and an error response
            self._save_messages_to_db(conversation.id, "user", user_input)
            self._save_messages_to_db(conversation.id, "assistant", "Sorry, I'm having trouble processing your request right now.")

            return {
                "conversation_id": str(conversation.id),
                "response": "Sorry, I'm having trouble processing your request right now.",
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error"
            }

    def _execute_add_task(self, args: dict) -> dict:
        """Execute the add_task function"""
        try:
            user_id = uuid.UUID(args["user_id"])
            title = args["title"]
            description = args.get("description", "")
            priority = args.get("priority", "medium")

            with next(get_session()) as session:
                # Verify user exists
                user = session.get(User, user_id)
                if not user:
                    return {"error": "User not found", "success": False}

                # Create new todo
                new_todo = Todo(
                    title=title,
                    description=description,
                    priority=priority,
                    user_id=user_id,
                    completed=False  # Default to not completed
                )

                session.add(new_todo)
                session.commit()
                session.refresh(new_todo)

                return {
                    "success": True,
                    "task_id": str(new_todo.id),
                    "message": f"Task '{title}' has been added successfully"
                }
        except Exception as e:
            return {"error": f"Failed to add task: {str(e)}", "success": False}

    def _execute_list_tasks(self, args: dict) -> dict:
        """Execute the list_tasks function"""
        try:
            user_id = uuid.UUID(args["user_id"])
            status_filter = args.get("status")

            with next(get_session()) as session:
                # Verify user exists
                user = session.get(User, user_id)
                if not user:
                    return {"error": "User not found", "success": False}

                # Build query
                query = select(Todo).where(Todo.user_id == user_id)

                if status_filter:
                    completed = status_filter.lower() == "completed"
                    query = query.where(Todo.completed == completed)

                todos = session.exec(query).all()

                task_list = []
                for todo in todos:
                    status = "completed" if todo.completed else "pending"
                    task_data = {
                        "id": str(todo.id),
                        "title": todo.title,
                        "description": todo.description,
                        "status": status,
                        "priority": todo.priority
                    }
                    task_list.append(task_data)

                return {
                    "success": True,
                    "tasks": task_list,
                    "total_count": len(task_list)
                }
        except Exception as e:
            return {"error": f"Failed to list tasks: {str(e)}", "success": False}

    def _execute_complete_task(self, args: dict) -> dict:
        """Execute the complete_task function"""
        try:
            user_id = uuid.UUID(args["user_id"])
            task_id = uuid.UUID(args["task_id"])

            with next(get_session()) as session:
                # Verify user exists
                user = session.get(User, user_id)
                if not user:
                    return {"error": "User not found", "success": False}

                # Find and update the task
                todo = session.get(Todo, task_id)
                if not todo:
                    return {"error": f"Task with ID {task_id} not found", "success": False}

                if todo.user_id != user_id:
                    return {"error": "Unauthorized: Task does not belong to user", "success": False}

                todo.completed = True
                session.add(todo)
                session.commit()

                return {
                    "success": True,
                    "message": f"Task '{todo.title}' has been marked as completed"
                }
        except Exception as e:
            return {"error": f"Failed to complete task: {str(e)}", "success": False}

    def _execute_delete_task(self, args: dict) -> dict:
        """Execute the delete_task function"""
        try:
            user_id = uuid.UUID(args["user_id"])
            task_id = uuid.UUID(args["task_id"])

            with next(get_session()) as session:
                # Verify user exists
                user = session.get(User, user_id)
                if not user:
                    return {"error": "User not found", "success": False}

                # Find and delete the task
                todo = session.get(Todo, task_id)
                if not todo:
                    return {"error": f"Task with ID {task_id} not found", "success": False}

                if todo.user_id != user_id:
                    return {"error": "Unauthorized: Task does not belong to user", "success": False}

                session.delete(todo)
                session.commit()

                return {
                    "success": True,
                    "message": f"Task '{todo.title}' has been deleted"
                }
        except Exception as e:
            return {"error": f"Failed to delete task: {str(e)}", "success": False}

    def _execute_update_task(self, args: dict) -> dict:
        """Execute the update_task function"""
        try:
            user_id = uuid.UUID(args["user_id"])
            task_id = uuid.UUID(args["task_id"])

            with next(get_session()) as session:
                # Verify user exists
                user = session.get(User, user_id)
                if not user:
                    return {"error": "User not found", "success": False}

                # Find the task to update
                todo = session.get(Todo, task_id)
                if not todo:
                    return {"error": f"Task with ID {task_id} not found", "success": False}

                if todo.user_id != user_id:
                    return {"error": "Unauthorized: Task does not belong to user", "success": False}

                # Update fields if provided
                if "title" in args:
                    todo.title = args["title"]
                if "description" in args:
                    todo.description = args["description"]
                if "status" in args:
                    todo.completed = args["status"].lower() == "completed"
                if "priority" in args:
                    todo.priority = args["priority"]
                if "due_date" in args:
                    todo.due_date = args["due_date"]

                session.add(todo)
                session.commit()

                return {
                    "success": True,
                    "message": f"Task '{todo.title}' has been updated"
                }
        except Exception as e:
            return {"error": f"Failed to update task: {str(e)}", "success": False}
    
    def _load_conversation_history(self, user_id: uuid.UUID, conversation_id: Optional[str] = None):
        """Load conversation and message history from database"""
        with next(get_session()) as session:
            if conversation_id:
                # Load existing conversation
                conv_uuid = uuid.UUID(conversation_id)
                conversation = session.get(Conversation, conv_uuid)
                
                if not conversation or conversation.user_id != user_id:
                    raise ValueError("Conversation not found or unauthorized")
            else:
                # Create new conversation
                conversation = Conversation(
                    user_id=user_id,
                    title="New Conversation"
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
            
            # Get messages for this conversation
            statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.timestamp)
            messages = session.exec(statement).all()
            
            # Update conversation title if it's still the default and we have messages
            if conversation.title == "New Conversation" and messages:
                # Use the first user message as the title (truncate if too long)
                first_user_msg = next((msg for msg in messages if msg.role == "user"), None)
                if first_user_msg and len(first_user_msg.content) > 0:
                    title = first_user_msg.content[:50] + "..." if len(first_user_msg.content) > 50 else first_user_msg.content
                    conversation.title = title
                    session.add(conversation)
                    session.commit()
        
        return conversation, messages
    
    def _format_messages_for_openai(self, db_messages, new_user_input):
        """Format database messages for OpenAI API"""
        formatted = [{"role": "system", "content": self.system_prompt}]
        
        for msg in db_messages:
            formatted.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add the new user input
        formatted.append({
            "role": "user",
            "content": new_user_input
        })
        
        return formatted
    
    def _save_messages_to_db(self, conversation_id: uuid.UUID, role: str, content: str):
        """Save a message to the database"""
        with next(get_session()) as session:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content
            )
            session.add(message)
            session.commit()
    
    def get_conversations(self, user_id: str) -> list:
        """Get all conversations for a user"""
        user_uuid = uuid.UUID(user_id)
        
        with next(get_session()) as session:
            statement = select(Conversation).where(Conversation.user_id == user_uuid).order_by(Conversation.updated_at.desc())
            conversations = session.exec(statement).all()
            
            return [{
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            } for conv in conversations]
    
    def get_conversation(self, conversation_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific conversation with its messages"""
        conv_uuid = uuid.UUID(conversation_id)
        user_uuid = uuid.UUID(user_id)
        
        with next(get_session()) as session:
            conversation = session.get(Conversation, conv_uuid)

            if not conversation or conversation.user_id != user_uuid:
                return None
            
            # Get messages for this conversation
            statement = select(Message).where(Message.conversation_id == conv_uuid).order_by(Message.timestamp)
            messages = session.exec(statement).all()
            
            return {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "messages": [{
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                } for msg in messages]
            }
    
    def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Delete a specific conversation"""
        conv_uuid = uuid.UUID(conversation_id)
        user_uuid = uuid.UUID(user_id)
        
        with next(get_session()) as session:
            conversation = session.get(Conversation, conv_uuid)

            if not conversation or conversation.user_id != user_uuid:
                return False
            
            session.delete(conversation)
            session.commit()
            
            return True