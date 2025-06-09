# demo-adk-app

_(This project is intentionally designed as a monorepo, i.e., has both the frontend and backend code in the same git repository. For a larger, more complex, or production-grade applications, separating frontends and backends into different repositories is often recommended for better team collaboration, independent scaling, and clearer separation of concerns.)_

> **Acknowledgement:**  
> This project makes use of the excellent [Deck of Cards API](https://deckofcardsapi.com/) by Chase Roberts. Many thanks to Chase for providing this fun and useful API!

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

cli> cc # this command creates a new conversation

cli> join <<conversation id>> # this command joins a conversation
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

1. Use the URL obtained from `make verify-frontend` in a browser

1. Login using the test user created in project setup

1. Join an existing conversation or create a new conversation

1. Converse with the agent to draw some cards from a deck, e.g.:

```bash
summarize what has happened so far
```

```bash
draw me 2 cards from a new deck
```

```bash
ok, add these drawn cards to a new pile John
```

```bash
draw 2 more cards and add them to pile Jane
```

```bash
ok, who has bigger hand, John or Jane? use simple card comparison, all colors are same, but cards have weight according to their number.
```

</details>

---

## The Power of LLM-based Agents as Middleware

This project, while simple in functionality, demonstrates the remarkable power of Large Language Models (LLMs) as middleware for backend services. The agent in this demo is able to:

- **Understand API Capabilities from Docstrings:**  
  The agent uses the docstrings of simple Python wrapper functions to understand what each API call does. No additional schema, OpenAPI spec, or manual translation is required—just clear function docstrings.

- **Interpret API Responses Directly:**  
  The agent can read and reason about the raw API responses (typically JSON), extracting the information it needs without any custom parsing or mapping logic.

- **Autonomously Orchestrate Workflows:**  
  Given a user request, the agent can decide which API(s) to call, in what order, and how to use the results—without any hardcoded rules or business logic. The LLM's reasoning ability enables it to create autonomous workflows on the fly.

Even though the functionality here is limited to drawing and shuffling cards, this is a powerful demonstration of how LLM-based agents can act as a universal interface layer for any backend service with reasonable API endpoints. With minimal glue code, LLMs can bridge the gap between natural language and programmatic APIs, opening up new possibilities for rapid prototyping, automation, and conversational interfaces.

> **Special thanks again to [Chase Roberts](https://deckofcardsapi.com/) for providing the Deck of Cards API, which made this demonstration possible. The open and well-documented API was essential in showcasing how LLM agents can interact with real-world services with minimal effort.**
