#### prompt - update test driver CLI to use token ####

modify the backend/test/cli.py test driver CLI as following:
- user needs to login first, before any CLI commands can be used
- ask user for email and password, then make the following HTTP request to get ID token (fetch FIREBASE_WEB_API_KEY from environment, give error if not present / set)
```bash
curl "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=$FIREBASE_WEB_API_KEY" \
-H 'Content-Type: application/json' \
--data-binary '{"email":"test@example.com", "password":"secret123","returnSecureToken":true}'
```
- save the idToken from response
- use the idToken in all API calls using Authorization with Beaer token

#### prompt - wire in authN/authZ in FastAPI endpoints ####

update FastAPI endpoing implementations in api/app.py as following:
- every endpoint will have a user injected from dependency get authenticated user method in auth module
- in the endpoints that have conversation id in resource path, will have session injected from get authenticated session method in auth module
- update methods where hardcoded user id was being used, to use user's uid


#### prompt - authN/authZ dependencies for FastAPI endpoints ####

add authnauthz module under backend/api/ to implement the following:
- module imports firebase_admin and firebase_admin.auth
- implements a method to initialize module with storing a reference to config object
- initializes firebase_admin(), no parameters uses default
- initializes security_scheme with HTTPBearer()
- defines an async dependency function to verify the firebase ID token as following:
```
async def get_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict
```
  - method takes http authorization header credentials
  - method verifies token in credentials using firebase_admin.auth.verify_id_token(token) method
  - method returns back verified token, which is a dictionary
- defines an async dependency function to implement authorization check for conversation as following:
```
async def get_authorized_session(conversation_id: Annotated[str,  Depends()], user: Annotated[dict, Depends(get_authenticated_user)]) -> Session
```
  - method takes conversation_id string and user details in dictionary from get_authenticated_user dependency
  - method retrieves session object from session service using conversation ID, user's uid and from config APP_NAME
  - method returns session object, if found, otherwise raises HTTP 404 not found exception


#### prompt - logic to initialize VertexAiRagMemoryService for ADK agents on cloud run ####
'''
modify pydantic object Config in utils.config as following:
- add new field named "RAG_CORPUS" of type str, it will be optional and set to None

modify get_memory_service method in services.provider as following:
- from vertexai import rag and check if an corpus already exists for project as folliwing:
```
resource_id: str | None = None
for item in rag.list_corpora():
  if item.display_name.startswith(config.APP_NAME):
    resource_id=item.name
    break
```
- if no corpus exists, then create new:
```
if not resource_id:
  embedding_model_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
       publisher_model="publishers/google/models/text-embedding-005"
    )
  )
  rag_corpus = rag.create_corpus(
      display_name=f"{config.APP_NAME}-corpus",
      backend_config=rag.RagVectorDbConfig(
         rag_embedding_model_config=embedding_model_config
      )
  )
  resource_id = rag_corpus.name
```
- Add resource ID to config object: `config.RAG_CORPUS=resource_id`
- when instantiating VertexAiRagMemoryService use named parameter rag_corpus=config.RAG_CORPUS in argument
'''


#### prompt - logic to use VertexAiSessionService for ADK Agents on Cloud Run ####
'''
modify pydantic object Config in utils.config as following:
- add new field named "AGENT_ID" of type str, it will be optional and set to None

modify get_session_service method in services.provider as following:
- import vertexai and initialize vertexai as following:
```
vertexai.init(
  project=config.GOOGLE_CLOUD_PROJECT,
  location=config.GOOGLE_CLOUD_LOCATION,
  staging_bucket=f"gs://{confg.APP_NAME}")
```
- from vertexai import agent_engines and check if an agent_engine resource already exists for project as folliwing:
```
resource_id: str | None = None
for item in agent_engines.list():
  resource_id=item.name
  break
```
- if no agent_engine resource exists, then create new:
```
if not resource_id:
  agent = agent_engines.create()
  resource_id = agent.name
```
- Add resource ID to config object: `config.AGENT_ID=resource_id`

modify api.app endpoint implementations, wherever it's using session_service methods, to use config.AGENT_ID as app_name when present, otherwise use config.APP_NAME, e.g.:
```
app_name=config.AGENT_ID if config.AGENT_ID else config.APP_NAME
session_service.create_session(app_name=app_name, ...)
session_service.list_sessions(app_name=app_name, ...)
```

similary modify services.runner wherever using app_name to use config.AGENT_ID as app_name when present
'''


#### prompt - changing environment variable names as per ADK expectation ####
'''
update README.md, backend/utils/config.py, Makefile and backend/cloudbuild.yaml files for following changes to environment variable names to be injected and used in deployed run time:
- use full name "GOOGLE_GENAI_USE_VERTEXAI" instead of "USE_VERTEXAI"
- use full name "GOOGLE_CLOUD_PROJECT" instead of "PROJECT_ID"
- use full name "GOOGLE_CLOUD_LOCATION" instead of "LOCATION"

Also update backend/servies/provider.py, backend/services/runner.py and backend/api/app.py to use correct GOOGLE_CLOUD_PROJECT name
'''

#### prompt - making test driver CLI easier ####
'''
modify test.cli logic to make it easier for user as following:
- use logic to work "in a conversation" and "out of conversation" modes
- default mode is "out of conversation" and commands require a conversation id parameter (Current behavior)
- give user a way to select "in a conversation" mode with a specific conversation id, which will be saved to use with send message command
- when in the "in a conversation" mode, only send message will be available and will use saved conversation id, user will not need to give command key word (e.g. "sm") or conv id, only provides text to send
- there will be some special command to get out of "in a conversation" mode, which takes user back to "out of conversation" mode
'''

#### prompt - concrete endpoint implementations ####
'''
make the placeholder implementations for api.app endpoints concrete as following:
- create_conversation will create a new instance of session object with session service using the “hard_coded_user-01” as the user id and APP_NAME from config, and use id and last_update_time from Session object to return new Conversation object
- get_conversations will use session service method list_sessions(*, app_name, user_id) using "hard_coded_user-01" as user id and APP_NAME from config and use the returned BaseModel's "sessions: List[Session]" to return back the list of sessions as an array of Conversation objects
- send_message will use conversation_id, "hard_coded_user-01" and APP_NAME to get Session object from session service and then call the invoke method on runner for returning back Message
- get_conversation_history will use conversation_id, "hard_coded_user-01" and APP_NAME to get Session object from session service and return back list of events from the “history” of the session object.
- delete_conversation will use conversation_id, "hard_coded_user-01" and APP_NAME to call delete_session method on session service
'''

#### prompt - wire up services and apps ####
'''
- modify api.app as following:
  - modify get_fast_api_app method to take parameters for runner: services.runner.Runner, session_service: BaseSessionService, memory_service: BaseMemoryService, artifact_service: BaseArtifactService, config: Config
  - references to these parameters should be saved for use in endpoint methods later
- update main.py as following:
  - initialize variables for session service, memory service, artifact service and root agent from services.provider module
  - initialize variables for services.runner.Runner instance
  - use the modified get_fast_api_app method with all appropriate parameters
'''


#### prompt - fixing invoke method ####
'''
re-implement the invoke method to use corred ADK specific logic using below sample code as an example:
```
  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")
```
for example:
- Message object needs to be changed to types.Content
- ADK runner's run_async need to be looped for events and processed appropriately
- only the final response event should be used to construct return Message
'''


##### prompt - add runner factory ####
'''
add a submodule runner.py under backend/services and implement class Runner as following:
- constructor initializes with parameters root_agent: BaseAgent, session_service: BaseSessionService, memory_service: BaseMemoryService, artifact_service: BaseArtifactService, config: Config
- implements an async method invoke as following:
  - takes input parameters session: google.adk.sessions.Session, msg: api.models.Message and return back Message
  - The method will instantiate a new google.adk.runners.Runner(*, app_name, agent, artifact_service=None, session_service, memory_service=None) using the parameters from class instance variables
  - the method will execute the “run_async” method on the runner using the “user_id” and “id” of the Session object and "text" of the msg object from the method parameter
  - The method will return the agent’s final response as a new Message object. If the agent returns a structured output, that output will be a JSON string conforming to the schema as part of the agent's contract with clients. Runner will be oblivious of any such contract, and will simply pass back the response as a string.
'''

##### prompt - add artifact service provider ####
'''
update backend/services/provider.py to implement method get_artifact_service that will do the following:
- takes input parameter config: Config
- returns an instance of BaseArtifactService from google.adk.artifacts module
- will create / initialize a singleton instance of artifacts service using below logic:
  - If config variable IS_TESTING is set, then return back instance of google.adk.artifacts.InMemoryArtifactService
  - else if config variable GCS_BUCKET is set and able to connect then return back instance of google.adk.artifacts.GcsArtifactService using GCS_BUCKET parameter
  - else fallback and return back instance of InMemoryArtifactService
'''


##### prompt - add memory service provider ####
'''
update backend/services/provider.py to implement method get_memory_service that will do the following:
- takes input parameter config: Config
- returns an instance of BaseMemoryService from google.adk.memory module
- will create / initialize a singleton instance of memory service using below logic:
  - If config variable “IS_TESTING” is set, then return back instance of google.adk.memory.InMemoryMemoryService
  - else if able to connect then return back instance of google.adk.memory.VertexAiRagMemoryService with default parameters
  - else fallback and return back instance of InMemoryMemoryService
'''


##### prompt - add session service provider ####
'''
update backend/services/provider.py to implement method get_session_service that will do the following:
- takes input parameter config: Config
- returns an instance of BaseSessionService from google.adk.sessions module
- will create / initialize a singleton instance of session service using below logic:
  - If config variable “IS_TESTING” is set, then return back instance of google.adk.sessions.InMemorySessionService
  - else if config variable “DB_URL” is set and able to connect, then return back instance of google.adk.sessions.DatabaseSessionService using DB_URL from config
  - else if config variable “DB_URL” is NOT set and able to connect then return back instance of google.adk.sessions.VertexAiSessionService using PROJECT_ID and LOCATION from config
  - else fallback and return back instance of InMemorySessionService
'''


##### prompt - add root agent provider ####
'''
add a submodule provider.py under backend/services and implement method get_root_agent that will do the following:
- takes input parameter config: Config
- returns an instance of BaseAgent
- will create/initialize a singleton reference for root_agent from simple_agent.agent module
- will use the singleton reference in return value
''' 

##### prompt - modify Dockerfile for FastAPI service #####
'''
Modify backend/Dockerfile for following:
- no need to inject environment variables, they will be injected during deployment
- add copying of following additional application code:
  - copy main.py
  - copy api/ directory
- modify startup to use command ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]

Modify backend/cloudbuild.yaml to use --ser-env-vars in run deploy command for following environment variables:
- export PROJECT_ID=$GOOGLE_CLOUD_PROJECT
- export LOCATION=$GOOGLE_CLOUD_LOCATION
- export USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI
- export APP_NAME=$GOOGLE_ADK_APP_NAME
- export CORS_ORIGINS='["http://localhost:3000", "$FIREBASE_APP_URL"]'
- export IS_TESTING=false
- export DECKOFCARDS_URL="https://deckofcardsapi.com/api/deck"
- export FIREBASE_KEY_JSON="{}"

Modify Makefile to pass the appropriate arguments for deploy-backend target
'''

##### prompt - create placeholder main app for FastAPI server #####
'''
Create a new main.py file under backend directory to do the following:
- get an instance of Config from utils.config module
- get an instance of FastAPI app from api.app module
- run the FastAPI app when execution is as __main__
- also make sure that FastAPI app can be run from command line using uvicorn directly
'''


##### prompt - create placeholder endpoints without authN/authZ #####
Modify api/app.py for following:

- add new model class Conversation with following fields:
  - conv_id: str # ID of session object created by session service
  - updated_at: datetime # last_updated_time of session object

- add create_conversation to handle POST /conversations and return back an instance of Conversation object

- add get_conversations to handle GET /conversations and return back a list of Conversation objects

- add new model class Message with following fields:
  - text: str # always required and should be sent in new message request

- add send_message to handle POST /conversations/{coonversation_id}/messages and return back instance of Message object

- add get_conversation_history to handle GET /conversations/{conversation_id}/history and return back list of Event objects imported from google.adk.events

- add delete_conversation to handle DELETE /conversations/{conversation_id} and return 204 no content

##### prompt - create placeholder FastAPI App Provider #####
- create a new submodule api.app under backend directory
- implement a method `get_fast_api_app` that takes parameter `config: Config` (from utils.config.Config) and returns back an instance of FastAPI
- the method will initialize and return a singleton instance of FastAPI app
- use a brief name for instance variable, example "_app"
- in app initialization use cors middleware with allow origins from config.CORS_ORIGINS
