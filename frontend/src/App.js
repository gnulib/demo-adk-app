import React, { useEffect, useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './App.css';
import LandingPage from './LandingPage';
import { auth, loginUser, logoutUser } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';
import apiClient from './apiClient'; // Import the API client

function App() {
  const [user, setUser] = useState(null);
  const [idToken, setIdToken] = useState('');
  const [isTokenVisible, setIsTokenVisible] = useState(false);

  // State for conversation UI
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [appError, setAppError] = useState(''); // To distinguish from LandingPage error

  const messagesEndRef = useRef(null); // For auto-scrolling

  // Login form state (email, password, error) is now managed by LandingPage
  // const [email, setEmail] = useState('');
  // const [password, setPassword] = useState('');
  // const [error, setError] = useState('');

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      setUser(currentUser);
      if (currentUser) {
        try {
          const token = await currentUser.getIdToken();
          setIdToken(token);
        } catch (error) {
          console.error("Error getting ID token:", error);
          setIdToken(''); // Clear token on error
        }
      } else {
        setIdToken(''); // Clear token on logout
      }
    });
    return () => unsubscribe(); // Cleanup subscription on unmount
  }, []);

  // handleLogin is now managed by LandingPage
  // const handleLogin = async (e) => { ... };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);


  // Fetch conversations when user logs in or currentConversationId is cleared
  useEffect(() => {
    if (user && !currentConversationId) {
      const fetchConversations = async () => {
        setIsLoading(true);
        setAppError('');
        try {
          const convos = await apiClient.getConversations();
          setConversations(convos || []); // Ensure convos is an array
        } catch (error) {
          console.error("Failed to fetch conversations:", error);
          setAppError(error.message || 'Failed to fetch conversations.');
          setConversations([]); // Clear conversations on error
        } finally {
          setIsLoading(false);
        }
      };
      fetchConversations();
    }
  }, [user, currentConversationId]);

  const handleLogout = async () => {
    try {
      await logoutUser();
      // onAuthStateChanged will set user to null
    } catch (err) {
      console.error("Logout error:", err);
      // setError('Failed to logout.'); // setError is not defined here, error state is in LandingPage
    }
  };

  if (!user) {
    return (
      <div className="App bg-gray-100 min-h-screen py-8 px-4 sm:px-6 lg:px-8">
        {/* LandingPage now includes the login form and manages its own layout */}
        <LandingPage loginUser={loginUser} />
      </div>
    );
  }

  // User is logged in
  // --- Handler Functions for Conversation UI ---

  const handleCreateConversation = async () => {
    setIsLoading(true);
    setAppError('');
    try {
      const newConversation = await apiClient.createConversation();
      if (newConversation && newConversation.conv_id) {
        setConversations(prev => [newConversation, ...prev]); // Add to list
        await handleEnterConversation(newConversation.conv_id); // Enter the new conversation
      }
    } catch (error) {
      console.error("Failed to create conversation:", error);
      setAppError(error.message || 'Failed to create conversation.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnterConversation = async (convId) => {
    setIsLoading(true); // Keep loading indicator for a brief moment for UI feedback
    setAppError('');
    setMessages([]); // Clear previous messages, start fresh
    try {
      // History fetching is removed. Conversation will start empty.
      setCurrentConversationId(convId);
    } catch (error) {
      // This catch block might be less relevant now but kept for safety
      console.error(`Error entering conversation ${convId}:`, error);
      setAppError(error.message || `Failed to enter conversation.`);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleDeleteConversation = async (convId) => {
    setIsLoading(true);
    setAppError('');
    try {
      await apiClient.deleteConversation(convId);
      setConversations(prev => prev.filter(c => c.conv_id !== convId));
      if (currentConversationId === convId) {
        setCurrentConversationId(null); // If current was deleted, go "outside"
        setMessages([]);
      }
    } catch (error) {
      console.error(`Failed to delete conversation ${convId}:`, error);
      setAppError(error.message || `Failed to delete conversation.`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !currentConversationId) return;

    const userMessage = {
      id: `temp-user-${Date.now()}`, // Temporary ID for UI
      text: newMessage,
      author: 'user',
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);
    setNewMessage('');
    setIsLoading(true); // Indicate agent is "thinking"
    setAppError('');

    try {
      // The backend expects a Message model: { text: string, author: string }
      const agentResponse = await apiClient.sendMessage(currentConversationId, { text: userMessage.text, author: 'user' });
      // The agentResponse should also be a Message model from the backend
      // We map it to our UI's message structure
      const formattedAgentMessage = {
        id: agentResponse.id || `agent-${Date.now()}`, // Use ID from response or generate
        text: agentResponse.text,
        author: 'agent',
        timestamp: agentResponse.timestamp || new Date().toISOString(),
      };
      setMessages(prev => [...prev, formattedAgentMessage]);
    } catch (error) {
      console.error("Failed to send message or get agent response:", error);
      setAppError(error.message || 'Failed to get response from agent.');
      // Optionally remove the user's message or add an error message to the chat
      setMessages(prev => [...prev, { id: `err-${Date.now()}`, text: `Error: ${error.message || 'Agent failed to respond.'}`, author: 'system', timestamp: new Date().toISOString() }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoBackToConversations = () => {
    setCurrentConversationId(null);
    setMessages([]);
    setAppError(''); // Clear errors when going back
  };

  // --- Render Logic ---
  return (
    <div className="App bg-gray-100 min-h-screen flex flex-col">
      {/* Main Content Area */}
      <div className="flex-grow w-full max-w-4xl mx-auto p-4 md:p-8 space-y-6 bg-white rounded-lg shadow-xl my-8">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">App Canvas</h1>

        {appError && <p className="text-sm text-red-600 text-center bg-red-100 p-3 rounded-md">{appError}</p>}
        {isLoading && <p className="text-sm text-blue-600 text-center">Loading...</p>}

        {!currentConversationId ? (
          // "Outside" Conversation Experience
          <div>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Your Conversations</h2>
            <button
              onClick={handleCreateConversation}
              disabled={isLoading}
              className="mb-6 w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            >
              Create New Conversation
            </button>
            {conversations.length === 0 && !isLoading && (
              <p className="text-gray-500 text-center">No conversations yet. Create one to get started!</p>
            )}
            <ul className="space-y-3">
              {conversations.map(conv => (
                <li key={conv.conv_id} className="p-4 bg-gray-50 rounded-md shadow-sm flex justify-between items-center">
                  <div>
                    <p className="font-medium text-gray-800">ID: {conv.conv_id}</p>
                    <p className="text-xs text-gray-500">Updated: {new Date(conv.updated_at).toLocaleString()}</p>
                  </div>
                  <div className="space-x-2">
                    <button
                      onClick={() => handleEnterConversation(conv.conv_id)}
                      disabled={isLoading}
                      className="bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded text-sm disabled:opacity-50"
                    >
                      Enter
                    </button>
                    <button
                      onClick={() => handleDeleteConversation(conv.conv_id)}
                      disabled={isLoading}
                      className="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded text-sm disabled:opacity-50"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          // "Inside" Conversation Experience
          <div className="flex flex-col h-[calc(100vh-250px)] md:h-[calc(100vh-300px)]"> {/* Adjust height as needed */}
            <button
              onClick={handleGoBackToConversations}
              className="mb-4 self-start bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              &larr; Back to Conversations
            </button>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">Conversation: {currentConversationId}</h2>
            
            {/* Messages Area */}
            <div className="flex-grow overflow-y-auto p-4 bg-gray-50 border border-gray-200 rounded-md mb-4 space-y-3">
              {messages.map((msg) => (
                <div key={msg.id} className={`flex ${msg.author === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-lg shadow ${
                    msg.author === 'user' ? 'bg-blue-500 text-white' : 
                    msg.author === 'agent' ? 'bg-green-500 text-white' : 'bg-gray-300 text-black' // System messages
                  }`}>
                    {msg.author === 'agent' ? (
                      <ReactMarkdown remarkPlugins={[remarkGfm]} className="prose prose-sm prose-invert max-w-none">
                        {msg.text}
                      </ReactMarkdown>
                    ) : (
                      <p className="text-sm">{msg.text}</p>
                    )}
                    <p className={`text-xs mt-1 ${
                      msg.author === 'user' ? 'text-blue-200' : 
                      msg.author === 'agent' ? 'text-green-200' : 'text-gray-500'
                    }`}>
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Message Input Form */}
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-grow p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !newMessage.trim()}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
              >
                Send
              </button>
            </form>
          </div>
        )}
      </div>

      {/* Footer for Sign Out and ID Token */}
      {user && (
        <div className="w-full max-w-4xl mx-auto p-4 md:p-8 text-center">
          <button
            onClick={handleLogout}
            className="mb-4 w-full md:w-auto bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Sign Out
          </button>
          {idToken && (
            <div className="w-full mt-2 p-4 bg-gray-200 rounded-md shadow">
              <button
                onClick={() => setIsTokenVisible(!isTokenVisible)}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium focus:outline-none"
              >
                {isTokenVisible ? 'Hide' : 'Show'} ID Token
              </button>
              {isTokenVisible && (
                <div className="mt-2 p-3 bg-gray-100 rounded">
                  <p className="text-xs text-gray-600 break-all">{idToken}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
