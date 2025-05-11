from google.adk.agents import BaseAgent
from google.adk.sessions import BaseSessionService, Session as AdkSession
from google.adk.memory import BaseMemoryService
from google.adk.artifacts import BaseArtifactService
from google.adk.runners import Runner as AdkRunner # Alias to avoid name collision

from utils.config import Config
from api.models import Message


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
        adk_runner = AdkRunner(
            agent=self._root_agent,
            session_service=self._session_service,
            memory_service=self._memory_service,
            artifact_service=self._artifact_service,
        )

        # Execute the agent run asynchronously
        # The user_id and session_id are sourced from the ADK Session object.
        agent_response_text = await adk_runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            request=msg.text,
        )

        # The agent's final response is returned as a string.
        # If the agent returns structured output, it will be a JSON string.
        # This Runner class remains oblivious to that contract and passes it as is.
        return Message(text=agent_response_text)
