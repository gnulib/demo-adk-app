# A Single Player Blackjack

This is a demo project to showcase building end-to-end application using Google ADK and Firebase. The application uses Firebase for user authentication and hosting react webapp, and LLM agents in the backend for running a single player game of Blackjack. **The primary objective of this project is to showcase how to architect, build, deploy and host an end to end solution for a conversational AI application on GCP infrastructure.**

**Acknowledgement:**
This project makes use of the excellent [Deck of Cards API](https://deckofcardsapi.com/) by Chase Roberts. Many thanks to Chase for providing this fun and useful API!

## Blog Series Companion
This repository serves as a hands-on companion for a 3-part blog series:
* **Part 1:** [The Agent Stack : Deploying Your First ADK Agent on Google Cloud](https://www.linkedin.com/pulse/agent-stack-deploying-your-first-adk-google-cloud-amit-bhadoria-emvdc) - is now live!
* **Part 2:** [The Agent Stack : Hosting a Secure Agent App with Firebase and Cloud Run](https://www.linkedin.com/pulse/agent-stack-hosting-secure-app-firebase-cloud-run-amit-bhadoria-cjvuc) - is now live!
* **Part 3:** The Agent Stack : Multi-Agent Orchestration & Autonomy - coming soon!

## Developer Setup

> Following is a one time developer setup required...

### Workspace Setup

<details>
<summary><b>Step 1:</b> clone the repo</summary>

```bash
git clone https://github.com/gnulib/demo-adk-app.git

cd demo-adk-app
```
</details>

<details>

<summary><b>Step 2:</b> initialize python environment for project</summary>

> create a python virtual environment within the repo project directory
```bash
python3 -m venv .venv
```

> activate python virtual environment
```bash
source .venv/bin/activate
```

> Install core development tools for project:

```bash
pip install --upgrade pip setuptools wheel build twine pip-tools
```

</details>

### Google Cloud Setup

Follow the steps listed in [GCP Setup](docs/GCP_SETUP.md) documentation for creating a Google Cloud Platform project and configuring appropriate APIs, roles, policies and storage buckets etc. required for this project.

### Firebase Setup

Follow the steps listed in [Firebase Setup](docs/FIREBASE_SETUP.md) documentation for creating a Firebase project linked to your Google Cloud Platform project created above, and configuring appropriate firebase project configurations.

### Project Setup

Add the backend application specific environment variables in `.env` file at the root of your project directory:

```bash
cat >> .env <<'EOF'
# Demo project specific environment variables
export APP_NAME=$GOOGLE_ADK_APP_NAME
export PORT=8000
export CORS_ORIGINS="http://localhost:3000, $FIREBASE_APP_URLS"
export IS_TESTING=true
export DECKOFCARDS_URL="https://deckofcardsapi.com/api/deck"
EOF
```

## Getting Started


> Following steps should be performed **_after_** [Workspace Setup](#workspace-setup), [GCP Setup](docs/GCP_SETUP.md) and [Firebase Setup](docs/FIREBASE_SETUP.md) steps are complete. If you have not completed those steps, please complete them before continuing here.

<details>

<summary>Install dependencies</summary>

> Activate project's virtual environment:

```bash
source .venv/bin/activate
```

> source project specific environment variables:

```bash
source .env
```

> Install backend agent app in editable mode:

```bash
pip install -e "./backend/src/demo_adk_app[dev]"
```

> Install frontend project dependencies:

```bash
(cd frontend;  npm install)
```

> New dependencies may have been added on top of earlier dependencies, hence need to install / update.

</details>

<details>
<summary>Test backend setup locally</summary>

> _In one terminal run the app locally for testing project setup_

```bash
(source .env; cd backend/src; uvicorn demo_adk_app.main:app --reload)
```

> _In another terminal run the test CLI for interacting with the app (use port from above)_

```bash
(export $(grep REACT_APP_FIREBASE_API_KEY frontend/.env); cd backend; python test/cli.py --port 8000)
```

> _Use the test CLI to interact with app_:

```bash
cli> help

cli> lc # this command lists existing conversations

cli> cc # this command creates and joins a new conversation

cli@9d9f5435-d569-4db2-b3b4-6cddf9c0e830> start a new game
```

> When you interact with the agent, if you get error like `google.genai.errors.ClientError: 403 PERMISSION_DENIED` -- this usually means either VertexAI API has not be enabled in your project, or your current environment is using a different google cloud project. Please make sure that you have completed all the steps mentioned above in "Google Cloud Setup" and are using the correct google project in your environment variables (`GOOGLE_CLOUD_PROJECT`) and with `gcloud` CLI _(check config in `gcloud config list` and `gcloud auth list`)_.

</details>

<details>

<summary>Test frontend setup locally</summary>

> _Once backend looks good, start frontend to interact with local agent service:_

```bash
(cd frontend; npm run start)
```
> _(above command uses `REACT_APP_BACKEND_URL` from `frontend/.env` file, and assumption is that local backend is running and listening on the same port mentioned in that variable. If port is different then modify the entry in `frontend/.env` file accordingly)_

> _(make sure that you have test user created as mentioned in [Firebase Setup](docs/FIREBASE_SETUP.md) above)_

> _Interact with the app frontend and confirm connectivity and functionality works as expected._

</details>

<details>

<summary>Deploy ADK app as Cloud Run Service</summary>

> Make sure that you have the following environment variables defined as described in the setup step above:
> * GOOGLE_ADK_APP_NAME
> * GOOGLE_CLOUD_LOCATION
> * GOOGLE_ADK_APP_REPOSITORY
> * GOOGLE_GENAI_USE_VERTEXAI
> * FIREBASE_APP_URLS

_Run the make target to build and deploy the backend:_

```bash
make deploy-backend
```

_Verify the status of cloud run service deployment:_

```bash
make verify-backend
```

</details>

<details>

<summary>Deploy ADK web app with Firebase hosting</summary>

> Make sure that you have the following environment variables defined as described in the Setup steps above:
> * GOOGLE_ADK_APP_NAME

_Run the make target to build and deploy the frontend:_

```bash
make deploy-frontend
```

_Verify the status of Firebase deployment:_

```bash
make verify-frontend
```

</details>

<details>

<summary>Interact with deployed app</summary>

> This app lets users play a game of Blackjack!

1. Use the URL obtained from `make verify-frontend` in a browser

1. Login using the test user created in project setup

1. Join an existing conversation or create a new conversation

1. Converse with the agent to play a game of Blackjack, e.g.:

```bash
tell me about this app
```

```bash
i want to start a new game
```

</details>

---

## The Power of Language Agents

This project, while simple in functionality, demonstrates the remarkable power of Language Agents:

- **Navigation through Natural Conversations:**
  The LLM agents are great at natural language understanding, and can provide a powerful conversational interface to end users for interacting with a backend system purely based on natural language conversation (no UI). The agents use basic building blocks of **memory**, **tools** and **state**, to create an experience for users to navigate the application in an easy and conversational manner.

- **Autonomously Orchestrate Workflows:**
  The multi-agent architecture uses LLM reasoning to determine how to delegate specific tasks to different agents. Given a user request, the LLM can decide which agent to delegate the request,
  which function / tool to call (if necessary), in what order, and with what parameters — without any hardcoded rules or business logic. The LLM's **reasoning ability** enables it to create autonomous workflows on the fly and respond to user's conversations naturally _**without prescribing** any specific navigation path or workflow_ to the user.

- **Understand Tool Capabilities Dynamically:**
  The agents use simple reflection on functions and pydantic models to
  understand what each tool / function call does. No additional schema, OpenAPI spec, or manual translation is required—just clear function docstrings. The agent can read and reason about the raw tool responses and memory data, extracting the information it needs without any custom parsing or mapping logic.

Even though the functionality here is limited to a single player game of Blackjack, this is a powerful demonstration of how LLM-based multi-agent systems can act as an autonmous system. With minimal glue code, LLMs can bridge the gap between natural language and task orchestration, opening up new possibilities for rapid prototyping, automation, and conversational interfaces.

> **Special thanks again to [Chase Roberts](https://deckofcardsapi.com/) for providing the Deck of Cards API, which made this demonstration possible.**
