import logging
import time
from typing import Dict
import traceback
from fastapi import Request

from google.adk.agents import BaseAgent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import BaseSessionService, Session as AdkSession
from google.adk.memory import BaseMemoryService
from google.adk.artifacts import BaseArtifactService
from google.adk.runners import Runner as AdkRunner # Alias to avoid name collision
from google.genai import types # For ADK Content and Part objects
from google.adk.events import Event, EventActions # Import Event for type hinting
from demo_adk_app.utils.config import Config
from demo_adk_app.utils.constants import StateVariables
from demo_adk_app.api.models import Message, StreamingEvent


def log_event(event: Event) -> str:
    """
    Helper function to log an ADK event in a readable format.

    Args:
        event: The ADK event to log.

    Returns:
        A formatted string representation of the event.
    """
    if event.content and event.content.parts:
        if event.get_function_calls():
            response = f"[Event] Author: {event.author}, Tool Call Requests:\n"
            for function_call in event.get_function_calls():
                response += f"Tool Name: {function_call.name} with Args: {function_call.args}\n"
            return response
        elif event.get_function_responses():
            response = f"[Event] Author: {event.author}, Tool Call Responses:\n"
            for function_response in event.get_function_responses():
                response += f"Tool Name: {function_response.name} Response: {function_response.response}\n"
            return response
    if event.error_message:
        return f"[Event] Author: {event.author}, Type: Error, Message: {event.error_message}"
    if event.actions and event.actions.escalate:
        return f"[Event] Author: {event.author}, Type: Escalation, Message: {event.error_message or 'No specific message.'}"
    if event.is_final_response():
        return f"[Event] Author: {event.author}, Type: Final Response,\nContent: {event.content.parts[0].text if event.content and event.content.parts else 'No content'}"
    elif event.partial and event.content and event.content.parts:
        return f"[Event] Author: {event.author}, Type: Partial Response,\nContent: {event.content.parts[0].text if event.content and event.content.parts else 'No content'}"
    return f"Unknown Event:\n{event}"

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

    async def invoke(self, user: Dict, session: AdkSession, msg: Message) -> Message:
        """
        Invokes the root agent with the given message within the provided session.

        Args:
            user: The authenticated user's details from Firebase ID token.
            session: The ADK session object for the current interaction.
            msg: The user's message to the agent.

        Returns:
            A Message object containing the agent's response.
        """
        app_name_to_use = self._config.AGENT_ID if self._config.AGENT_ID else self._config.APP_NAME
        # make sure that session has user's details for tools to use
        if not session.state.get(StateVariables.USER_DETAILS, None):
            current_time = time.time()
            state_changes = {
                StateVariables.USER_DETAILS: user,
                StateVariables.USER_ID: user.get("email", None)
            }
            actions_with_update = EventActions(state_delta=state_changes)
            system_event = Event(
                invocation_id="user_details_update",
                author='system',
                actions=actions_with_update,
                timestamp=current_time
            )
            await self._session_service.append_event(
                session=session,
                event=system_event,
            )
            session = await self._session_service.get_session(
                app_name=app_name_to_use,
                user_id=session.user_id,
                session_id=session.id
            )
            logger.info(f"Updated session {session.id} with state: {session.state}")

        # Instantiate the ADK Runner
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
        try:
            async for event in adk_runner.run_async(
                user_id=session.user_id, session_id=session.id,
                new_message=content,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE)
            ):
                # # accumulate the full response text if needed
                # if event.content and event.content.parts:
                #     full_response_text += ''.join(part.text for part in event.content.parts if part.text)
                if event.error_message:
                    full_response_text += f"\n[Event] Author: {event.author}, Type: Error, Message: {event.error_message}\n"

                # You can uncomment the line below to see *all* events during execution
                logger.info(log_event(event))

                # Key Concept: is_final_response() marks the concluding message for the turn.
                if event.is_final_response():
                    #### in case of SSE / streaming, partial response is being collected
                    # if event.content and event.content.parts:
                    #     # full_response_text += "\n" + ''.join(part.text for part in event.content.parts if part.text)
                    #     full_response_text = event.content.parts[0].text
                    if event.actions and event.actions.escalate:  # Handle potential errors/escalations
                        full_response_text += f"\nAgent escalated: {event.error_message or 'No specific message.'}\n"
                    #### in case of SSE, we just keep looping until run_async does EOF and loop ends itself
                    #### no need to explicitly break the loop
                    # if event.turn_complete:
                    #     logger.info("Turn complete, returning response to user.")
                    #     break  # Stop processing events once the final response is found
                else:
                    if event.partial and event.content and event.content.parts:
                        text = ''.join(part.text for part in event.content.parts if part.text)
                        full_response_text += text
                    elif event.actions and event.actions.transfer_to_agent:
                        full_response_text += f"\n{event.author} transferring to {event.actions.transfer_to_agent} ...\n"
                    elif event.get_function_calls():
                        for function in event.get_function_calls():
                            full_response_text += f"\n{event.author} calling function: {function.name} ...\n" if function.name != "transfer_to_agent" else ""

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            raise e

        # The agent's final response is returned as a string.
        # If the agent returns structured output, it will be a JSON string.
        # This Runner class remains oblivious to that contract and passes it as is.
        return Message(text=full_response_text)

    async def submit(self, user: Dict, session: AdkSession, msg: Message) -> StreamingEvent:
        """
        Submit a user message for processing with streaming.

        Args:
            user: The authenticated user's details from Firebase ID token.
            session: The ADK session object for the current interaction.
            msg: The user's message to the agent.

        Returns:
            A StreamingEvent object containing submission result.
        """
        state_changes = {
                StateVariables.LAST_USER_MESSAGE: msg,
            }
        # make sure that session has user's details for tools to use
        if not session.state.get(StateVariables.USER_DETAILS, None):
            state_changes[StateVariables.USER_DETAILS] = user
            state_changes[StateVariables.USER_ID] = user.get("uid", None)
        actions_with_update = EventActions(state_delta=state_changes)
        current_time = time.time()
        system_event = Event(
            invocation_id="last_user_message_submit",
            author='system',
            actions=actions_with_update,
            timestamp=current_time
        )
        await self._session_service.append_event(
            session=session,
            event=system_event,
        )
        app_name_to_use = self._config.AGENT_ID if self._config.AGENT_ID else self._config.APP_NAME
        session = await self._session_service.get_session(
            app_name=app_name_to_use,
            user_id=session.user_id,
            session_id=session.id
        )
        logger.info(f"Updated session {session.id} with state: {session.state}")
        return StreamingEvent(type="start", data=msg)

    async def stream(self, user: Dict, session: AdkSession, msg: Message, request: Request):
        """
        Yields StreamingEvent from agents when processing latest user submitted message

        Args:
            user: The authenticated user's details from Firebase ID token.
            session: The ADK session object for the current interaction.
            msg: The user's message to the agent.

        Returns:
            None (events are yielded while processing, no return at end of processing)
        """
        # fetch the last user submitted message from session state
        last_usr_msg = session.state.get(StateVariables.LAST_USER_MESSAGE, None)
        if not last_usr_msg:
            logger.info("there is no last user message to process")
            yield StreamingEvent(type="error", data="no user message for processing")
            return
        if not session.state.get(StateVariables.USER_DETAILS, None):
            logger.error("last user message was submitted without user's details")
            yield StreamingEvent(type="error", data="no user details for processing")
            return

        # clear last user message from session state
        actions_with_update = EventActions(state_delta={
                StateVariables.LAST_USER_MESSAGE: msg,
        })
        current_time = time.time()
        system_event = Event(
            invocation_id="last_user_message_clear",
            author='system',
            actions=actions_with_update,
            timestamp=current_time
        )
        await self._session_service.append_event(
            session=session,
            event=system_event,
        )
        app_name_to_use = self._config.AGENT_ID if self._config.AGENT_ID else self._config.APP_NAME
        session = await self._session_service.get_session(
            app_name=app_name_to_use,
            user_id=session.user_id,
            session_id=session.id
        )
        logger.info(f"Updated session {session.id} with state: {session.state}")

        # Instantiate the ADK Runner
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
        try:
            async for event in adk_runner.run_async(
                user_id=session.user_id, session_id=session.id,
                new_message=content,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE)
            ):
                # make sure that client is still connected
                if await request.is_disconnected():
                    logger.info("streaming client disconnected, closing connection")
                    return
                # # accumulate the full response text if needed
                # if event.content and event.content.parts:
                #     full_response_text += ''.join(part.text for part in event.content.parts if part.text)
                if event.error_message:
                    yield StreamingEvent(type="error", data=f"[Event] Author: {event.author}, Type: Error, Message: {event.error_message}")
                    full_response_text += f"\n[Event] Author: {event.author}, Type: Error, Message: {event.error_message}\n"

                # You can uncomment the line below to see *all* events during execution
                logger.info(log_event(event))

                # Key Concept: is_final_response() marks the concluding message for the turn.
                if event.is_final_response():
                    #### in case of SSE / streaming, partial response is being collected
                    # if event.content and event.content.parts:
                    #     # full_response_text += "\n" + ''.join(part.text for part in event.content.parts if part.text)
                    #     full_response_text = event.content.parts[0].text
                    if event.actions and event.actions.escalate:  # Handle potential errors/escalations
                        yield StreamingEvent(type="action", data=f"Agent escalated: {event.error_message or 'No specific message.'}")
                        full_response_text += f"\nAgent escalated: {event.error_message or 'No specific message.'}\n"
                    #### in case of SSE, we just keep looping until run_async does EOF and loop ends itself
                    #### no need to explicitly break the loop
                    # if event.turn_complete:
                    #     logger.info("Turn complete, returning response to user.")
                    #     break  # Stop processing events once the final response is found
                else:
                    if event.partial and event.content and event.content.parts:
                        text = ''.join(part.text for part in event.content.parts if part.text)
                        yield StreamingEvent(type="message", data=text)
                        full_response_text += text
                    elif event.actions and event.actions.transfer_to_agent:
                        yield StreamingEvent(type="action", data=f"{event.author} transferring to {event.actions.transfer_to_agent} ...")
                        full_response_text += f"\n{event.author} transferring to {event.actions.transfer_to_agent} ...\n"
                    elif event.get_function_calls():
                        for function in event.get_function_calls():
                            yield StreamingEvent(type="action", data=f"{event.author} calling function: {function.name} ..." if function.name != "transfer_to_agent" else "")
                            full_response_text += f"\n{event.author} calling function: {function.name} ...\n" if function.name != "transfer_to_agent" else ""

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            raise e

        # The agent's final response is returned as a string.
        yield StreamingEvent(type="end", data=full_response_text)

        return
