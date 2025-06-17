import requests
import json
import readline # For better input experience
from sseclient import SSEClient # For Server-Sent Events
import sys
import os
import argparse

# BASE_URL will be initialized in main().
BASE_URL: str = "" # Placeholder, will be set in main()
ACTIVE_CONVERSATION_ID: str | None = None # None for "out of conversation" mode
ID_TOKEN: str | None = None # To store the Firebase ID token

def set_active_conversation(conv_id: str):
    """Sets the active conversation ID."""
    global ACTIVE_CONVERSATION_ID
    ACTIVE_CONVERSATION_ID = conv_id
    print(f"Joined conversation {ACTIVE_CONVERSATION_ID}. Type 'leave' to exit conversation mode.")
def print_response(response: requests.Response):
    """Helper to print API response."""
    print(f"Status Code: {response.status_code}")
    if not response.text:
        print("Response: No content")
        print("-" * 20)
        return

    try:
        data = response.json()  # Attempt to parse as JSON
        # Check if the response is specifically a Message object (e.g., from send_message)
        # which is a dictionary with a single key "text".
        if isinstance(data, dict) and len(data) == 1 and "text" in data:
            print("Response Text:")
            # Print the text content directly. This allows newlines (\n)
            # and other standard Python string escapes within the text to be rendered.
            print(data["text"])
        else:
            # For other JSON responses, pretty-print the whole JSON structure.
            print("Response JSON:")
            print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        # If response.json() fails, it's not a valid JSON string.
        print("Response Text (not JSON):")
        print(response.text)
    print("-" * 20)

def create_conversation():
    """Calls POST /conversations"""
    print("Creating a new conversation...")
    headers = {}
    if ID_TOKEN:
        headers["Authorization"] = f"Bearer {ID_TOKEN}"
    try:
        response = requests.post(f"{BASE_URL}/conversations", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                for index, conversation in enumerate(data):
                    print(f"{index}: {conversation.get('conv_id')}")
            else:
                print("Unexpected response format.")
        else:
            print_response(response)
        if response.status_code == 201:  # Assuming 201 Created is the success status code
            data = response.json()
            conv_id = data.get("conv_id")
            if conv_id:
                set_active_conversation(conv_id)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def get_conversations():
    """Calls GET /conversations"""
    print("Fetching all conversations...")
    headers = {}
    if ID_TOKEN:
        headers["Authorization"] = f"Bearer {ID_TOKEN}"
    try:
        response = requests.get(f"{BASE_URL}/conversations", headers=headers)
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def send_message(conv_id: str, text: str):
    """Calls POST /conversations/{conversation_id}/messages"""
    if not conv_id or not text:
        print("Usage: send_message <conversation_id> <text>")
        return
    print(f"Sending message to conversation {conv_id}...")
    headers = {}
    if ID_TOKEN:
        headers["Authorization"] = f"Bearer {ID_TOKEN}"
    
    payload = {"text": text, "author": "user"}

    try:
        # 1. Submit the message
        print(f"Submitting message to conversation {conv_id}...")
        submit_url = f"{BASE_URL}/conversations/{conv_id}/submit"
        submit_response = requests.post(submit_url, json=payload, headers=headers)
        print("Submit Response:")
        print_response(submit_response)

        if submit_response.status_code != 200: # Or whatever success code /submit returns, assuming 200 for now
            print(f"Failed to submit message, status code: {submit_response.status_code}")
            return

        # 2. Stream the response
        print(f"Streaming response from conversation {conv_id}...")
        stream_url = f"{BASE_URL}/conversations/{conv_id}/stream"
        
        # SSEClient needs headers for authorization.
        # The stream endpoint also expects the message content as query parameters.
        stream_params = payload 
        
        try:
            sse_headers = headers.copy() # Use the same auth headers
            # sseclient-py typically handles 'Accept': 'text/event-stream'
            
            client = SSEClient(stream_url, params=stream_params, headers=sse_headers)
            for event in client:
                if not event.data: # Skip empty keep-alive messages if any
                    continue
                try:
                    # Assuming event.data is a JSON string representing a Message like {"text": "...", "author": "..."}
                    event_data_json = json.loads(event.data)
                    if "text" in event_data_json:
                        # Try to mimic the direct text output style from print_response
                        print(f"Agent: {event_data_json['text']}")
                    elif "type" in event_data_json and event_data_json["type"] == "ToolCall": # Example for other event types
                        print(f"Tool Call: {event_data_json.get('name')}") # Adjust based on actual ToolCall structure
                    elif "type" in event_data_json and event_data_json["type"] == "ToolResult": # Example for other event types
                        print(f"Tool Result: {event_data_json.get('name')}") # Adjust based on actual ToolResult structure
                    else:
                        # If not the expected Message format, print raw JSON
                        print(f"Stream data: {json.dumps(event_data_json, indent=2)}")
                except json.JSONDecodeError:
                    # If not JSON, print raw data
                    print(f"Stream data: {event.data}")
                except Exception as e_inner:
                    print(f"Error processing stream event data: {e_inner}")
                    print(f"Raw event data: {event.data}")
            print("-" * 20) # End of streaming response
        except requests.exceptions.RequestException as e_sse:
            print(f"Error during streaming: {e_sse}")
        except Exception as e_general:
            print(f"An unexpected error occurred during streaming: {e_general}")

    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server (submit phase): {e}")
    except Exception as e_outer:
        print(f"An unexpected error occurred (submit phase): {e_outer}")


def get_conversation_history(conv_id: str):
    """Calls GET /conversations/{conversation_id}/history"""
    if not conv_id:
        print("Usage: get_history <conversation_id>")
        return
    print(f"Fetching history for conversation {conv_id}...")
    headers = {}
    if ID_TOKEN:
        headers["Authorization"] = f"Bearer {ID_TOKEN}"
    try:
        response = requests.get(f"{BASE_URL}/conversations/{conv_id}/history", headers=headers)
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def delete_conversation(conv_id: str):
    """Calls DELETE /conversations/{conversation_id}"""
    if not conv_id:
        print("Usage: delete_conversation <conversation_id>")
        return
    print(f"Deleting conversation {conv_id}...")
    headers = {}
    if ID_TOKEN:
        headers["Authorization"] = f"Bearer {ID_TOKEN}"
    try:
        response = requests.delete(f"{BASE_URL}/conversations/{conv_id}", headers=headers)
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def print_help():
    """Prints available commands."""
    print("\nAvailable commands:")
    print("--- Out of Conversation Mode ---")
    print("  cc                                   - Create a new conversation.")
    print("  lc                                   - List all conversations.")
    print("  sm <conv_id> <message>               - Send a message to a specific conversation.")
    print("  gh <conv_id>                         - Get history for a specific conversation.")
    print("  dc <conv_id>                         - Delete a specific conversation.")
    print("  join <conv_id>                       - Enter 'in a conversation' mode with specified ID.")
    print("  url <new_base_url>                   - Change the API base URL (current: " + BASE_URL + ").")
    print("  h, help                              - Show this help message.")
    print("  q, exit                              - Exit the CLI.")
    print("\n--- In a Conversation Mode (after using 'join <conv_id>') ---")
    print("  <your message text>                  - Send message to the active conversation.")
    print("  leave                                - Exit 'in a conversation' mode.")
    print("  h, help                              - Show this help message (shows all commands).")
    print("  q, exit                              - Exit the CLI.\n")

def main():
    global BASE_URL, ACTIVE_CONVERSATION_ID, ID_TOKEN

    parser = argparse.ArgumentParser(description="Interactive API CLI client.")
    parser.add_argument("--host", type=str, default="localhost",
                        help="The host of the API server (default: localhost).")
    parser.add_argument("--port", type=int,
                        help="The port of the API server. If not provided, port is omitted from the URL (standard HTTP/HTTPS ports assumed).")
    
    cli_args = parser.parse_args()

    host = cli_args.host
    port_to_use = cli_args.port # This will be None if --port is not provided

    scheme = ""
    if not host.startswith("http://") and not host.startswith("https://"):
        scheme = "http://" # Default to http if no scheme provided

    if port_to_use is not None:
        BASE_URL = f"{scheme}{host}:{port_to_use}"
        print(f"Using port {port_to_use} from command-line argument.")
    else:
        BASE_URL = f"{scheme}{host}"
        if not scheme and (host.startswith("http://") or host.startswith("https://")):
             print("Port not specified via --port argument. Omitting port from URL.")
        else:
             print("Port not specified via --port argument. Omitting port from URL (standard HTTP/HTTPS ports will be assumed).")
    
    print(f"Using API base URL: {BASE_URL}")

    # Firebase Authentication
    firebase_api_key = os.getenv("REACT_APP_FIREBASE_API_KEY")
    if not firebase_api_key:
        print("Error: REACT_APP_FIREBASE_API_KEY environment variable not set. Cannot authenticate.")
        sys.exit(1)
    firebase_api_key = firebase_api_key.strip('"')
    email = input("Enter Firebase Email: ").strip()
    password = input("Enter Firebase Password: ").strip() # Consider using getpass for hidden input

    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
    auth_payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        print("Authenticating with Firebase...")
        auth_response = requests.post(auth_url, json=auth_payload)
        auth_response.raise_for_status() # Raise an exception for HTTP errors
        auth_data = auth_response.json()
        ID_TOKEN = auth_data.get("idToken")
        if not ID_TOKEN:
            print("Login failed: idToken not found in response.")
            print_response(auth_response)
            sys.exit(1)
        print("Successfully authenticated with Firebase.")
        print("-" * 20)
    except requests.exceptions.HTTPError as e:
        print(f"Firebase authentication failed: {e.response.status_code}")
        print_response(e.response)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to Firebase authentication service: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Firebase authentication: {e}")
        sys.exit(1)

    print("Interactive API CLI. Type 'help' for commands, 'exit' to quit.")
    
    while True:
        try:
            prompt = f"cli@{ACTIVE_CONVERSATION_ID}> " if ACTIVE_CONVERSATION_ID else "cli> "
            user_input = input(prompt).strip()
            if not user_input:
                continue

            if ACTIVE_CONVERSATION_ID: # In a conversation mode
                if user_input.lower() == "leave":
                    print(f"Leaving conversation {ACTIVE_CONVERSATION_ID}.")
                    ACTIVE_CONVERSATION_ID = None
                elif user_input.lower() in ["h", "help"]:
                    print_help()
                elif user_input.lower() in ["q", "exit"]:
                    print("Exiting.")
                    break
                else: # Treat as message text
                    send_message(ACTIVE_CONVERSATION_ID, user_input)
            else: # Out of conversation mode
                parts = user_input.split(" ", 2)
                command = parts[0].lower()
                args = parts[1:]

                if command in ["q", "exit"]:
                    print("Exiting.")
                    break
                elif command in ["h", "help"]:
                    print_help()
                elif command == "cc": # create_conversation
                    create_conversation()
                elif command == "lc": # get_conversations
                    get_conversations()
                elif command == "sm": # send_message
                    if len(args) < 2:
                        print("Usage: sm <conversation_id> <text>")
                    else:
                        send_message(args[0], args[1])
                elif command == "gh": # get_history
                    if len(args) < 1:
                        print("Usage: gh <conversation_id>")
                    else:
                        get_conversation_history(args[0])
                elif command == "dc": # delete_conversation
                    if len(args) < 1:
                        print("Usage: dc <conversation_id>")
                    else:
                        delete_conversation(args[0])
                elif command == "join":
                    if len(args) < 1:
                        print("Usage: join <conversation_id>")
                    else:
                        if args[0].isdigit():
                            index = int(args[0])
                            response = requests.get(f"{BASE_URL}/conversations", headers={"Authorization": f"Bearer {ID_TOKEN}"})
                            if response.status_code == 200:
                                data = response.json()
                                if 0 <= index < len(data):
                                    ACTIVE_CONVERSATION_ID = data[index].get('conv_id')
                                    print(f"Joined conversation {ACTIVE_CONVERSATION_ID}. Type 'leave' to exit conversation mode.")
                                else:
                                    print("Invalid index.")
                            else:
                                print("Failed to fetch conversations.")
                        else:
                            # Optional: Could add a check here to see if conv_id is valid
                            # by trying to fetch its history or details.
                            ACTIVE_CONVERSATION_ID = args[0]
                            print(f"Joined conversation {ACTIVE_CONVERSATION_ID}. Type 'leave' to exit conversation mode.")
                elif command == "url":
                    if len(args) < 1:
                        print(f"Current base URL: {BASE_URL}")
                        print("Usage: url <new_base_url>")
                    else:
                        BASE_URL = args[0]
                        print(f"API base URL changed to: {BASE_URL}")
                else:
                    print(f"Unknown command: {command}. Type 'h' or 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except EOFError: # Handle Ctrl+D
            print("\nExiting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
