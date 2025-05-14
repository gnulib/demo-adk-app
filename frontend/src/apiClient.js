import { auth } from './firebase'; // To get the ID token

const BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

// Helper function to get the ID token
const getIdToken = async () => {
  const currentUser = auth.currentUser;
  if (currentUser) {
    return await currentUser.getIdToken();
  }
  return null;
};

// Helper function for making API requests
const makeRequest = async (url, method = 'GET', body = null) => {
  const token = await getIdToken();
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    method,
    headers,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${BASE_URL}${url}`, config);
    if (!response.ok) {
      // Try to parse error response from backend if available
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // If response is not JSON, use status text
        errorData = { detail: response.statusText };
      }
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    // For DELETE requests with 204 No Content, response.json() will fail
    if (response.status === 204) {
      return null; 
    }

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      return await response.json();
    } else {
      // If response.ok is true, but content is not JSON, this is unexpected.
      const responseText = await response.text(); // Get the actual response text
      throw new Error(
        `Expected JSON response from server, but received ${contentType || 'unknown content type'}. ` +
        `Status: ${response.status}. Response body: ${responseText.substring(0, 200)}...` // Log part of the unexpected response
      );
    }
  } catch (error) {
    console.error(`API request error for ${method} ${url}:`, error.message); // Log error.message for clarity
    throw error; // Re-throw the error to be caught by the caller
  }
};

// API client methods
export const apiClient = {
  createConversation: async () => {
    return makeRequest('/conversations', 'POST');
  },

  getConversations: async () => {
    return makeRequest('/conversations', 'GET');
  },

  sendMessage: async (conversationId, messageRequest) => {
    // messageRequest should be an object like { text: "Hello", author: "user" }
    // The backend expects a Message model, which includes `text` and `author`.
    // Ensure the message_request structure matches the backend's Message model.
    // For example: { "text": "Hello there!", "author": "user" }
    return makeRequest(`/conversations/${conversationId}/messages`, 'POST', messageRequest);
  },

  getConversationHistory: async (conversationId) => {
    return makeRequest(`/conversations/${conversationId}/history`, 'GET');
  },

  deleteConversation: async (conversationId) => {
    return makeRequest(`/conversations/${conversationId}`, 'DELETE');
  },
};

export default apiClient;
