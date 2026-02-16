"use client";

import { useAuth } from "@/context/AuthContext";
import { useState, useRef, useEffect } from "react";
import { useRouter } from 'next/navigation';
import { apiClient, ChatMessage, Conversation as ConversationType } from "@/lib/api";
import Navigation from "@/components/Navigation";

const ChatPage = () => {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [inputMessage, setInputMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<ConversationType[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversations when user is available
  useEffect(() => {
    if (user) {
      loadConversations();
    }
  }, [user]);

  // Scroll to bottom of messages when they change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const loadConversations = async () => {
    try {
      const data = await apiClient.getConversations();
      setConversations(data);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadConversation = async (conversationId: string) => {
    try {
      const data = await apiClient.getConversation(conversationId);
      setActiveConversationId(data.id);
      setMessages(data.messages || []);
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const createNewConversation = () => {
    setActiveConversationId(null);
    setMessages([]);
    setSidebarOpen(false); // Close sidebar on new conversation
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage,
    };

    // Add user message to UI immediately
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputMessage("");
    setIsLoading(true);

    try {
      // Send message to backend API
      const response = await apiClient.sendMessage(inputMessage, activeConversationId || undefined);

      // Add bot response to messages
      const botMessage: ChatMessage = {
        role: "assistant",
        content: response.response,
      };
      
      setMessages(prev => [...prev, botMessage]);
      setActiveConversationId(response.conversation_id);
      
      // Refresh conversations list
      loadConversations();
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp?: string) => {
    if (!timestamp) return new Date().toLocaleTimeString();
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (authLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (!user) {
    router.push('/');
    return null;
  }

  return (
    <div className="flex h-screen flex-col bg-gray-50">
      <Navigation />
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        {sidebarOpen && (
          <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-[calc(100vh-4rem)]">
            <div className="p-4 border-b border-gray-200">
              <button
                onClick={createNewConversation}
                className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition-colors flex items-center justify-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                New Chat
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto">
              <div className="p-2">
                <h3 className="text-sm font-medium text-gray-500 px-2 mb-2">Recent Chats</h3>
                {conversations.length === 0 ? (
                  <p className="text-sm text-gray-500 px-2 py-4">No conversations yet</p>
                ) : (
                  <ul>
                    {conversations.map((conv) => (
                      <li key={conv.id}>
                        <button
                          onClick={() => loadConversation(conv.id)}
                          className={`w-full text-left p-2 rounded-md text-sm ${
                            activeConversationId === conv.id
                              ? "bg-blue-100 text-blue-700"
                              : "hover:bg-gray-100 text-gray-700"
                          }`}
                        >
                          <div className="font-medium truncate">{conv.title.substring(0, 30)}{conv.title.length > 30 ? '...' : ''}</div>
                          <div className="text-xs text-gray-500">
                            {new Date(conv.updated_at).toLocaleDateString()}
                          </div>
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
            
            <div className="p-4 border-t border-gray-200">
              <div className="flex items-center">
                <div className="mr-3">
                  <div className="bg-gray-200 border-2 border-dashed rounded-xl w-8 h-8" />
                </div>
                <div className="text-sm">
                  <div className="font-medium text-gray-700">{user.email}</div>
                  <div className="text-gray-500">AI Chat Assistant</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="bg-white border-b border-gray-200 p-4 flex items-center">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="mr-4 p-2 rounded-md hover:bg-gray-100"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            )}
            <h1 className="text-xl font-semibold text-gray-800">AI Todo Assistant</h1>
            <div className="ml-auto flex space-x-2">
              <button
                onClick={createNewConversation}
                className="p-2 rounded-md hover:bg-gray-100 text-gray-600"
                title="New Chat"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </header>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 bg-gradient-to-b from-blue-50 to-indigo-50">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center">
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mb-4" />
                <h3 className="text-xl font-medium text-gray-700 mb-2">How can I help you today?</h3>
                <p className="text-gray-500 max-w-md text-center">
                  Ask me to add, list, complete, or manage your to-dos. Try: "Add a task to buy groceries" or "What do I have to do?"
                </p>
              </div>
            ) : (
              <div className="max-w-3xl mx-auto space-y-6">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-xl p-4 ${
                        msg.role === 'user'
                          ? 'bg-blue-500 text-white rounded-tr-none'
                          : 'bg-white text-gray-800 rounded-tl-none shadow-sm'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{msg.content}</div>
                      <div
                        className={`text-xs mt-1 ${
                          msg.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                        }`}
                      >
                        {formatTime(msg.timestamp)}
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-[80%] rounded-xl rounded-tl-none bg-white text-gray-800 shadow-sm p-4">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-100"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="bg-white border-t border-gray-200 p-4">
            <div className="max-w-3xl mx-auto">
              <div className="flex rounded-lg border border-gray-300 bg-white p-1 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Message AI Todo Assistant..."
                  className="flex-1 border-0 focus:ring-0 resize-none max-h-32 py-2 px-3"
                  rows={1}
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className={`self-end m-1 p-2 rounded-md ${
                    inputMessage.trim()
                      ? 'bg-blue-500 text-white hover:bg-blue-600'
                      : 'text-gray-400'
                  }`}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                  </svg>
                </button>
              </div>
              <div className="mt-2 text-xs text-gray-500 text-center">
                AI Assistant can help you manage your to-dos. Try: "Add a task to call mom", "Show me my tasks", or "Mark task as complete"
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;