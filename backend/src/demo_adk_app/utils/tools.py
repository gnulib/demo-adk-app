# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The 'memorize' tool for several agents to affect session states."""

from datetime import datetime
import json
import os
from typing import Optional

from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext
from .constants import StateVariables
from .models import GameRoom


def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Stored "{key}": "{value}"'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def forget(key: str, value: str, tool_context: ToolContext):
    """
    Forget pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be removed.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    if tool_context.state[key] is None:
        tool_context.state[key] = []
    if value in tool_context.state[key]:
        tool_context.state[key].remove(value)
    return {"status": f'Removed "{key}": "{value}"'}

def initialize_session_state_for_instruction_prompts(callback_context: CallbackContext):
    """
    Sets up the initial state with all variables that are being used in the instruction prompts
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is constructed.

    NOTE: this is not required, using '?' to make state variables optional in prompt

    Args:
        callback_context: The callback context.
    """
    state = callback_context.state
    variables = [v for v in vars(StateVariables) if not v.startswith("__")]

    for variable in variables:
        key = getattr(StateVariables, variable)
        if not key in state:
            print(f"initializing variable: {key}")
            state[key] = None
    return None

def _load_game_room(game_room_id: str, tool_context: ToolContext):
    """
    utility method to load game room object
    Args:
        game_room_id: a game room id to load the game
        tool_context: The ADK tool context.
    Returns:
        game_room: if successfule
        error: if failure
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # check if game room exists (app scope)
    # TODO: replace this from "app:" scope to DB store
    # game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    game_room_dict = state.get(f"{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return None, {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }

    # convert to pydantic model
    game_room = GameRoom.model_validate(game_room_dict)
    return game_room, None

def _save_game_room(game_room: GameRoom, tool_context: ToolContext):
    """
    utility method to save game room object
    Args:
        game_room: a game room object to save
        tool_context: The ADK tool context.
    Returns:
        None
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # TODO: replace this from "app:" scope to DB store
    # state[f"{State.APP_PREFIX}{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()
    state[f"{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()
