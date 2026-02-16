"""Chat API Endpoint for AI-Powered Todo Chatbot"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
import uuid

from app.db.database import get_session
from app.core.agent import TodoAgent
from app.core.auth import get_current_user
from app.models.user import User
from app.models.conversation import ConversationResponse, MessageResponse


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(
    message: str,
    conversation_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process a chat message and return a response from the AI agent.
    
    Args:
        message: The user's message
        conversation_id: Optional conversation ID (creates new if None)
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with conversation ID and AI response
    """
    if not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        # Initialize the agent
        agent = TodoAgent()
        
        # Process the chat request
        result = agent.process_chat_request(
            user_input=message,
            user_id=str(current_user.id),
            conversation_id=conversation_id
        )
        
        return result
    
    except ValueError as e:
        # Handle specific validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Log the error in a real application
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


@router.get("/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user)
):
    """
    List all conversations for the current user.
    
    Args:
        current_user: The authenticated user
    
    Returns:
        List of conversations
    """
    try:
        agent = TodoAgent()
        conversations = agent.get_conversations(str(current_user.id))
        return conversations
    
    except Exception as e:
        # Log the error in a real application
        print(f"Error listing conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving conversations"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific conversation with its messages.
    
    Args:
        conversation_id: The ID of the conversation
        current_user: The authenticated user
    
    Returns:
        Conversation details with messages
    """
    try:
        agent = TodoAgent()
        conversation = agent.get_conversation(conversation_id, str(current_user.id))
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return conversation
    
    except ValueError:
        # Invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    
    except Exception as e:
        # Log the error in a real application
        print(f"Error getting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the conversation"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific conversation.
    
    Args:
        conversation_id: The ID of the conversation to delete
        current_user: The authenticated user
    
    Returns:
        Success message
    """
    try:
        agent = TodoAgent()
        success = agent.delete_conversation(conversation_id, str(current_user.id))
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return {"message": "Conversation deleted successfully"}
    
    except ValueError:
        # Invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    
    except Exception as e:
        # Log the error in a real application
        print(f"Error deleting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the conversation"
        )