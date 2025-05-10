# demo-adk-app

_(This project is intentionally designed as a monorepo, i.e., has both the frontend and backend code in the same git repository. For a larger, more complex, or production-grade applications, separating frontends and backends into different repositories is often recommended for better team collaboration, independent scaling, and clearer separation of concerns.)_

> **Acknowledgement:**  
> This project makes use of the excellent [Deck of Cards API](https://deckofcardsapi.com/) by Chase Roberts. Many thanks to Chase for providing this fun and useful API!

## Blog Series Companion
This repository serves as a hands-on companion for a 3-part blog series.
*   **Part 1:** [The Agent Stack : Deploying Your First ADK Agent on Google Cloud](https://www.linkedin.com/pulse/agent-stack-deploying-your-first-adk-google-cloud-amit-bhadoria-emvdc) - is now live!
*   To follow the hands-on exercises for Part 1, please check out the specific code state using the following git command:
     ```bash
     git checkout tags/blog-part-1
     ```
> This command creates a new detached copy of project code from the `blog-part-1` tag, allowing you to work through the exercises.

## Developer Setup

> Following is a one time developer setup required on top of setup done with following parts of the blog series...
>
> * Google Cloud Setup from Part - 1 : [link to README with tag blog-part-1](https://github.com/gnulib/demo-adk-app/blob/blog-part-1/README.md)
>
> ⚠️ **IMPORTANT:** If you have not completed the previous parts, please complete them before continuing here.

<details>
<summary>Google Cloud Setup</summary>

**Step 1:** Export environment variables related to project:

```bash
# use same values as previous setup instructions
```

> You can add the above exports into your shell's environment file, e.g. `~/.zshrc`

**Step 2:** Enable the following APIs in your project:

```bash
# use same command as previous setup instructions
```

**Step 3:** Verify your configurations:

```bash
gcloud config list # verify gcloud is using correct google cloud account and project

gcloud artifacts repositories list # verify artifact repository exists
```

> Above command will display your current `gcloud` configuration, including the active account and the project, and the default region/zone if you set them. These should match the project and google cloud account you are using for this demo.

**Step 4:** Add necessary roles to service account:

```bash
# use same roles as previous setup instructions
```

**Step 5:** Add necessary secret key access to service account:

```bash
# No secret key access to be added yet.
```

</details>

## Project Setup

> Following is project specific setup required on top of setup done with Part - 1 of the blog series. If you have not completed the previous parts, please complete them before continuing here.

<details>

<summary>Install dependencies</summary>

_Install backend project dependencies:_

```bash
pip install -r backend/requirements.txt
```

> New dependencies may have been added on top of earlier dependencies, hence need to install / update.

</details>

<details>

<summary>Setup local environment</summary>

_create `backend/.env` file for local testing:_

```bash
cat > backend/.env <<'EOF'
export PROJECT_ID=$GOOGLE_CLOUD_PROJECT
export LOCATION=$GOOGLE_CLOUD_LOCATION
export USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI
export APP_NAME=$GOOGLE_ADK_APP_NAME
export PORT=8000
export CORS_ORIGINS="[\"http://localhost:3000\", \"$FIREBASE_APP_URL\"]"
export IS_TESTING=true
export DECKOFCARDS_URL="https://deckofcardsapi.com/api/deck"
export FIREBASE_KEY_JSON="{}"
EOF
```

</details>

## Getting Started
> You'll be using two terminals, besides any IDE you might be using to view / navigate project files. One terminal will be used to run `aider` for any copilot help (e.g., asking to help describe code), and another terminal will be where you'll be running the frontend / backend apps for local testing.

<details>
<summary>Start aider on terminal</summary>

_(assuming you configured alias in aider setup above)_

```bash
copilot
```

> First time invocation of `aider` may require installing additional packages, let that complete.

_Ask `aider` to describe project..._

```bash
> describe the project to me 
```

> This documentation assumes you are using aider on a terminal window as a copilot for learning about project, or making changes to project as per your needs.

</details>

<details>
<summary>Test Project Setup Locally</summary>

_In one terminal run the app locally for testing project setup_

```bash
(cd backend; source .env; python main.py)
```

_In another terminal run the test CLI for interacting with the app (use port from above)_

```bash
(cd backend; source .env; python test/cli.py --port 8000)
```

> When you interact with the agent, if you get error like `google.genai.errors.ClientError: 403 PERMISSION_DENIED` -- this usually means either VertexAI API has not be enabled in your project, or your current environment is using a different google cloud project. Please make sure that you have completed all the steps mentioned above in "Google Cloud Setup" and are using the correct google project in your environment variables (`GOOGLE_CLOUD_PROJECT`) and with `gcloud` CLI _(check config in `gcloud config list` and `gcloud auth list`)_.

</details>

<details>

<summary>Deploy ADK app as Cloud Run Service</summary>

> Make sure that you have the following environment variables defined as described in the Google Cloud Setup step above:
> * GOOGLE_ADK_APP_NAME
> * GOOGLE_CLOUD_LOCATION
> * GOOGLE_ADK_APP_REPOSITORY
> * GOOGLE_GENAI_USE_VERTEXAI

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

<summary>Interact with ADK app</summary>

> Use the service URL obtained from `make verify-backend` (look for the `url:` field), or extract it directly using: `gcloud run services describe "$GOOGLE_ADK_APP_NAME-service" --platform managed --region $GOOGLE_CLOUD_LOCATION --format='value(status.url)'`

**Step 1:** Browse to the service URL.

**Step 2:** From "Select an agent" drop down pick `simple_agent`.

**Step 3:** Converse with the agent to draw some cards from a deck, e.g.:

```
draw me 2 cards from a new deck
```

```
ok, add these drawn cards to a new pile John
```

```
draw 2 more cards and add them to pile Jane
```

```
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
