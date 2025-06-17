import { auth } from './firebase'; // To get the ID token

const rawBaseUrl = process.env.REACT_APP_BACKEND_URL || '';
// Strip any inline comments starting with '#' and then trim whitespace
const commentStartIndex = rawBaseUrl.indexOf('#');
const cleanedBaseUrl = commentStartIndex !== -1 ? rawBaseUrl.substring(0, commentStartIndex) : rawBaseUrl;
const BASE_URL = cleanedBaseUrl.trim();

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

  // Renamed from sendMessage and now calls the /submit endpoint
  submitMessage: async (conversationId, messageRequest) => {
    // messageRequest should be an object like { text: "Hello", author: "user" }
    return makeRequest(`/conversations/${conversationId}/submit`, 'POST', messageRequest);
  },

  streamConversationEvents: async (conversationId, messagePayload, { onEvent, onError, onOpen, onClose }) => {
    const token = await getIdToken();
    if (!token) {
      if (onError) onError(new Error("Authentication token not available."));
      return null; // Return null if no token, so caller knows not to proceed.
    }

    // messagePayload is {text: "...", author: "..."}
    const queryParams = new URLSearchParams({
      ...messagePayload, 
      token: token, // Pass token as query param - backend /stream needs to support this
    });
    const url = `${BASE_URL}/conversations/${conversationId}/stream?${queryParams.toString()}`;

    const eventSource = new EventSource(url);

    eventSource.onopen = (event) => {
      console.log("SSE connection opened for conversation events:", event);
      if (onOpen) onOpen(event);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data);
        // parsedData is expected to be like: { type: "message" | "action" | "error" | "end", data: any }
        if (onEvent) onEvent(parsedData);

        if (parsedData.type === "end") {
          console.log("SSE stream indicated end by server.");
          if (onClose) onClose(); // Notify App.js that the stream has naturally ended
          eventSource.close(); 
        }
      } catch (e) {
        console.error("Error parsing SSE event data:", e, "Raw data:", event.data);
        if (onError) onError(new Error(`Error parsing SSE event data: ${e.message}. Raw: ${event.data.substring(0,100)}`));
        // Don't close eventSource here for a single bad message, unless it's a policy.
        // The main eventSource.onerror will handle connection-level errors.
      }
    };

    eventSource.onerror = (errorEvent) => {
      // This handles network errors or if the server closes the connection abruptly without "end" event.
      console.error("SSE connection error:", errorEvent);
      if (onError) onError(new Error("SSE connection failed.")); // Pass a generic error or the event itself
      eventSource.close(); // Close on error
      if (onClose) onClose(); // Also notify App.js that the stream is now closed
    };

    return eventSource; // Return for manual close if needed (e.g., component unmount, new message send)
  },

  getConversationHistory: async (conversationId) => {
    return makeRequest(`/conversations/${conversationId}/history`, 'GET');
  },

  deleteConversation: async (conversationId) => {
    return makeRequest(`/conversations/${conversationId}`, 'DELETE');
  },
};

export default apiClient;
