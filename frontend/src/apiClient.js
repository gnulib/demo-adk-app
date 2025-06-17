import { auth } from './firebase'; // To get the ID token
import { fetchEventSource } from '@microsoft/fetch-event-source';

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

  streamConversationEvents: async (
    conversationId,
    messagePayload, // {text: "...", author: "..."}
    { onEvent, onError, onOpen, onClose, abortSignal } // abortSignal is from AbortController
  ) => {
    const token = await getIdToken();
    if (!token) {
      if (onError) onError(new Error("Authentication token not available."));
      // No EventSource object to return, so App.js needs to handle this possibility
      return; 
    }

    // messagePayload (text, author) is still sent as query parameters
    const queryParams = new URLSearchParams(messagePayload);
    const url = `${BASE_URL}/conversations/${conversationId}/stream?${queryParams.toString()}`;

    const headers = {
      'Authorization': `Bearer ${token}`,
      // 'Accept': 'text/event-stream', // fetchEventSource adds this by default
    };

    try {
      await fetchEventSource(url, {
        method: 'GET',
        headers,
        signal: abortSignal, // For aborting the request
        openWhenHidden: false, // Don't keep connection open if tab is not visible

        onopen: async (response) => {
          if (response.ok) {
            console.log("SSE connection opened with fetchEventSource:", response);
            if (onOpen) onOpen(response);
          } else {
            // Handle non-2xx responses before streaming starts
            const errorText = await response.text();
            console.error(`SSE connection failed to open: ${response.status}`, errorText);
            if (onError) onError(new Error(`SSE connection failed: ${response.status} ${errorText.substring(0,100)}`));
            // fetchEventSource will not proceed if onopen throws or response is not ok
            // and it doesn't call onclose/onerror in this specific path.
            // So, we also need to call onClose here to ensure App.js cleans up.
            if (onClose) onClose();
            throw new Error(`Server error ${response.status}: ${errorText}`); // This will be caught by the outer try/catch
          }
        },

        onmessage: (event) => { // event is an EventSourceMessage
          try {
            // event.event is the event name (e.g., 'message', 'update')
            // event.data is the data string
            // event.id is the event ID
            // event.retry is the retry timeout
            if (!event.data) return; // Skip empty keep-alive messages if any

            const parsedData = JSON.parse(event.data);
            // parsedData is expected to be like: { type: "message" | "action" | "error" | "end", data: any }
            if (onEvent) onEvent(parsedData);

            if (parsedData.type === "end") {
              console.log("SSE stream indicated end by server (via fetchEventSource).");
              // No need to manually close, fetchEventSource handles it.
              // The onclose callback will be triggered.
            }
          } catch (e) {
            console.error("Error parsing SSE event data (fetchEventSource):", e, "Raw data:", event.data);
            if (onError) onError(new Error(`Error parsing SSE event data: ${e.message}. Raw: ${event.data.substring(0,100)}`));
          }
        },

        onclose: () => {
          // This is called when the connection is closed, either by the server,
          // by abortSignal, or if openWhenHidden is false and tab becomes hidden.
          console.log("SSE connection closed (fetchEventSource).");
          if (onClose) onClose();
        },

        onerror: (err) => {
          // This is called for network errors or other fatal errors during the connection.
          // It will also be called if onopen throws.
          console.error("SSE connection error (fetchEventSource):", err);
          if (onError) onError(err instanceof Error ? err : new Error("SSE connection failed."));
          // fetchEventSource will automatically retry on certain errors unless err.eventPhase is EventSource.CLOSED
          // or if the error is rethrown from here. If we want to stop retries, we should throw.
          // For simplicity, we let it retry if it can, but App.js's onError will have been called.
          // If the error is from onopen (non-2xx), we've already called onClose.
          // If it's a different error, onClose will be called by the onclose callback eventually.
          // Throwing the error here will stop retries and cause the promise from fetchEventSource to reject.
          throw err; 
        },
      });
    } catch (err) {
      // This catches errors from fetchEventSource if it fails to connect or if onerror rethrows.
      console.error("fetchEventSource promise rejected or setup failed:", err);
      // Ensure onError and onClose are called if not already by the callbacks
      // This is a fallback.
      if (onError) onError(err instanceof Error ? err : new Error("SSE stream setup failed"));
      if (onClose) onClose();
    }
  },

  getConversationHistory: async (conversationId) => {
    return makeRequest(`/conversations/${conversationId}/history`, 'GET');
  },

  deleteConversation: async (conversationId) => {
    return makeRequest(`/conversations/${conversationId}`, 'DELETE');
  },
};

export default apiClient;
