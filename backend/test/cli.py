import requests
import json
import readline # For better input experience
import sys
import os
import argparse

# BASE_URL will be initialized in main().
BASE_URL: str = "" # Placeholder, will be set in main()
ACTIVE_CONVERSATION_ID: str | None = None # None for "out of conversation" mode

def print_response(response: requests.Response):
    """Helper to print API response."""
    print(f"Status Code: {response.status_code}")
    if not response.text:
        print("Response: No content")
        print("-" * 20)
        return

    try:
        data = response.json() # Attempt to parse as JSON
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
    try:
        response = requests.post(f"{BASE_URL}/conversations")
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def get_conversations():
    """Calls GET /conversations"""
    print("Fetching all conversations...")
    try:
        response = requests.get(f"{BASE_URL}/conversations")
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def send_message(conv_id: str, text: str):
    """Calls POST /conversations/{conversation_id}/messages"""
    if not conv_id or not text:
        print("Usage: send_message <conversation_id> <text>")
        return
    print(f"Sending message to conversation {conv_id}...")
    try:
        payload = {"text": text}
        response = requests.post(f"{BASE_URL}/conversations/{conv_id}/messages", json=payload)
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def get_conversation_history(conv_id: str):
    """Calls GET /conversations/{conversation_id}/history"""
    if not conv_id:
        print("Usage: get_history <conversation_id>")
        return
    print(f"Fetching history for conversation {conv_id}...")
    try:
        response = requests.get(f"{BASE_URL}/conversations/{conv_id}/history")
        print_response(response)
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to the server: {e}")

def delete_conversation(conv_id: str):
    """Calls DELETE /conversations/{conversation_id}"""
    if not conv_id:
        print("Usage: delete_conversation <conversation_id>")
        return
    print(f"Deleting conversation {conv_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/conversations/{conv_id}")
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
    global BASE_URL, ACTIVE_CONVERSATION_ID

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
        scheme = "http://"

    if port_to_use is not None:
        BASE_URL = f"{scheme}{host}:{port_to_use}"
        print(f"Using port {port_to_use} from command-line argument.")
    else:
        BASE_URL = f"{scheme}{host}" # Port is omitted
        if not scheme: # Host already had a scheme
             print("Port not specified via --port argument. Omitting port from URL.")
        else:
             print("Port not specified via --port argument. Omitting port from URL (standard HTTP/HTTPS ports will be assumed).")


    print("Interactive API CLI. Type 'help' for commands, 'exit' to quit.")
    print(f"Using API base URL: {BASE_URL}")

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
