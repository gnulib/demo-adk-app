import requests
import json
import readline # For better input experience
from ..utils.config import get_config

# BASE_URL will be initialized in main() using configuration.
BASE_URL: str = "" # Placeholder, will be set in main()

def print_response(response: requests.Response):
    """Helper to print API response."""
    try:
        print(f"Status Code: {response.status_code}")
        if response.text:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Response: No content")
    except json.JSONDecodeError:
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
    print("  create_conversation                  - Create a new conversation.")
    print("  get_conversations                    - List all conversations.")
    print("  send_message <conv_id> <message>     - Send a message to a conversation.")
    print("  get_history <conv_id>                - Get history for a conversation.")
    print("  delete_conversation <conv_id>        - Delete a conversation.")
    print("  url <new_base_url>                   - Change the API base URL (current: " + BASE_URL + ").")
    print("  help                                 - Show this help message.")
    print("  exit                                 - Exit the CLI.\n")

def main():
    global BASE_URL

    # Load configuration and set BASE_URL
    try:
        app_config = get_config()
        BASE_URL = f"http://localhost:{app_config.PORT}"
        print(f"Successfully loaded port {app_config.PORT} from configuration.")
    except Exception as e:
        default_port = 8000 # Default port if config fails
        print(f"Warning: Could not load configuration to determine port: {e}")
        print(f"Falling back to default port: {default_port}")
        BASE_URL = f"http://localhost:{default_port}"

    print("Interactive API CLI. Type 'help' for commands, 'exit' to quit.")
    print(f"Using API base URL: {BASE_URL}")

    while True:
        try:
            user_input = input("cli> ").strip()
            if not user_input:
                continue

            parts = user_input.split(" ", 2)
            command = parts[0].lower()
            args = parts[1:]

            if command == "exit":
                print("Exiting.")
                break
            elif command == "help":
                print_help()
            elif command == "create_conversation":
                create_conversation()
            elif command == "get_conversations":
                get_conversations()
            elif command == "send_message":
                if len(args) < 2:
                    print("Usage: send_message <conversation_id> <text>")
                else:
                    send_message(args[0], args[1])
            elif command == "get_history":
                if len(args) < 1:
                    print("Usage: get_history <conversation_id>")
                else:
                    get_conversation_history(args[0])
            elif command == "delete_conversation":
                if len(args) < 1:
                    print("Usage: delete_conversation <conversation_id>")
                else:
                    delete_conversation(args[0])
            elif command == "url":
                if len(args) < 1:
                    print(f"Current base URL: {BASE_URL}")
                    print("Usage: url <new_base_url>")
                else:
                    BASE_URL = args[0]
                    print(f"API base URL changed to: {BASE_URL}")
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")

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
