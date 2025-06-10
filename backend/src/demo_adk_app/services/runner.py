import logging

from google.adk.agents import BaseAgent
from google.adk.sessions import BaseSessionService, Session as AdkSession
from google.adk.memory import BaseMemoryService
from google.adk.artifacts import BaseArtifactService
from google.adk.runners import Runner as AdkRunner # Alias to avoid name collision
from google.genai import types # For ADK Content and Part objects

from demo_adk_app.utils.config import Config
from demo_adk_app.api.models import Message

# Get a logger instance for this module
logger = logging.getLogger(__name__)

class Runner:
    """
    A class to encapsulate the execution of an agent using the ADK Runner.
    """

    def __init__(
        self,
        root_agent: BaseAgent,
        session_service: BaseSessionService,
        memory_service: BaseMemoryService,
        artifact_service: BaseArtifactService,
        config: Config,
    ):
        """
        Initializes the Runner.

        Args:
            root_agent: The root agent to be executed.
            session_service: The session service for managing session state.
            memory_service: The memory service for agent memory.
            artifact_service: The artifact service for handling artifacts.
            config: The application configuration.
        """
        self._root_agent = root_agent
        self._session_service = session_service
        self._memory_service = memory_service
        self._artifact_service = artifact_service
        self._config = config # Stored if needed for future runner configurations

    async def invoke(self, session: AdkSession, msg: Message) -> Message:
        """
        Invokes the root agent with the given message within the provided session.

        Args:
            session: The ADK session object for the current interaction.
            msg: The user's message to the agent.

        Returns:
            A Message object containing the agent's response.
        """
        # Instantiate the ADK Runner
        app_name_to_use = self._config.AGENT_ID if self._config.AGENT_ID else self._config.APP_NAME
        adk_runner = AdkRunner(
            app_name=app_name_to_use,
            agent=self._root_agent,
            session_service=self._session_service,
            memory_service=self._memory_service,
            artifact_service=self._artifact_service,
        )

        # Prepare the user's message in ADK format
        content = types.Content(role='user', parts=[types.Part(text=msg.text)])

        full_response_text = ""  # To accumulate all parts of the response

        # Key Concept: run_async executes the agent logic and yields Events.
        # We iterate through events to find the final answer.
        async for event in adk_runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            # accumulate the full response text if needed
            if event.content and event.content.parts:
                full_response_text += ''.join(part.text for part in event.content.parts if part.text)

            # You can uncomment the line below to see *all* events during execution
            logger.info("  [Event] Author: %s, Type: %s, Final: %s,\nContent: %s", event.author, type(event).__name__, event.is_final_response(), event.content)

            # Key Concept: is_final_response() marks the concluding message for the turn.
            if event.is_final_response():
                if event.actions and event.actions.escalate:  # Handle potential errors/escalations
                    full_response_text += f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
                break  # Stop processing events once the final response is found
        
        # The agent's final response is returned as a string.
        # If the agent returns structured output, it will be a JSON string.
        # This Runner class remains oblivious to that contract and passes it as is.
        return Message(text=full_response_text)
