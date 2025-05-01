# demo-adk-app

> **Acknowledgement:**  
> This project makes use of the excellent [Deck of Cards API](https://deckofcardsapi.com/) by Chase Roberts. Many thanks to Chase for providing this fun and useful API!

This is a demo project for a simple app using [Google's ADK](https://google.github.io/adk-docs/) framework. This project is intended to demonstrate how to setup a GCP project for deploying ADK app as a cloud run service.

Secondary objective of this project is to demonstrate the power of LLMs, how they can be used to build conversation interface against pretty much any service that has reasonable APIs.

> This project is intentionally designed as a monorepo, i.e., has both the frontend and backend code in the same git repository. For a larger, more complex, or production-grade applications, separating frontends and backends into different repositories is often recommended for better team collaboration, independent scaling, and clearer separation of concerns.

## Developer Setup

> Following is a one time developer setup required to install appropriate tools and configurations on local machine, and to get Google Cloud resources created...

<details>
<summary>Google Cloud Setup</summary>

> You'll be required to have a Google Cloud project, either in your own personal account, or your enterprise / work related account, as following ...

**Step 1:** Create a new [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and enable billing.

> If you are an individual developer, you should be able to signup for a new Google Cloud by [getting started for free](https://cloud.google.com/free) program.

**Step 2:** Install [gcloud](https://cloud.google.com/sdk/docs/install) on your local development machine and initialize gcloud to use the new project created above

> If you already have gcloud installed / configured from your work account and you want to following this example project in your personal account, then you might want to create a new configuration (in addition to existing work configuration) with `gcloud init` using your personal google cloud account.

**Step 3:** Export environment variables related to project:

```bash
export GOOGLE_CLOUD_PROJECT="<<<YOUR_GOOGLE_PROJECT_CREATED_ABOVE>>>"
export GOOGLE_CLOUD_LOCATION="<<<<LOCATION_TO_USE>>>" #e.g. us-central1
export GOOGLE_CLOUD_PROJECT_NUMBER="$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format='value(projectNumber)')"
export GOOGLE_ADK_APP_REPOSITORY="adk-apps"
export GOOGLE_ADK_APP_NAME="demo-adk-app"
export GOOGLE_GENAI_USE_VERTEXAI="True"
```

> You can add the above exports into your shell's environment file, e.g. `~/.zshrc`

**Step 4:** Set your default Google Cloud project for subsequent steps:

```bash
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

**Step 5:** Generate a local Application Default Credentials (ADC) file to be used for VertexAI API calls:

```bash
gcloud auth application-default login
```

**Step 6:** Enable the Cloud Build, Cloud Run, Artifact Registry and VertexAI APIs in your project:

```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com
```

**Step 7:** Create a repository in Artifact Registry to store your ADK app images:

```bash
gcloud artifacts repositories create $GOOGLE_ADK_APP_REPOSITORY --repository-format=docker --location=$GOOGLE_CLOUD_LOCATION --description="ADK applications container repository"
```

> If you get a message that the repository already exists, you can ignore above step.

**Step 8:** Verify your configurations:

```bash
gcloud config list # verify gcloud is using correct google cloud account and project

gcloud artifacts repositories list # verify artifact repository exists
```

> Above command will display your current `gcloud` configuration, including the active account and the project, and the default region/zone if you set them. These should match the project and google cloud account you are using for this demo.

**Step 9:** Add IAM role to service account:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/run.admin \
  --condition=None
```

</details>

<details>

<summary>aider Setup</summary>

> This project uses [aider](https://aider.chat/) as a copilot for learning about project, or making changes to project as per your needs. You can configure aider to use any of the supported LLMs. In this example we are assuming you are using one of the following two options...

<details>
<summary> Option 1: aider with Vertex AI gemini model</summary>

> This is the preferred option, since you'll be working off of the google cloud project for ADK app, it makes sense to use the same for aider...

**Step 1:** Install [aider](https://aider.chat/) on your development machine:

```bash
python -m pip install aider-install

aider-install
```

**Step 2:** Export environment variables (in this example we'll use VertexAI APIs with aider):

```bash
export VERTEXAI_PROJECT=$GOOGLE_CLOUD_PROJECT # assuming already defined with gcloud setup
export VERTEXAI_LOCATION=$GOOGLE_CLOUD_LOCATION # assuming already defined with gcloud setup
export AIDER_MODEL="vertex_ai/gemini-2.5-pro-exp-03-25" # (this one is free because it's experimental)
```

**Step 3:** Create an alias to invoke aider:

```bash
alias copilot="aider --model $AIDER_MODEL"
```

> You can add the above exports and alias in your shell's environment file, e.g. `~/.zshrc`

</details>
<details>
<summary>Option 2: aider with OpenAI gpt model</summary>

> If you already have a paid developer account with OpenAI with existing credits purchased, then you can use OpenAI LLMs for aider...

**Step 1:** Install [aider](https://aider.chat/):

```bash
python -m pip install aider-install

aider-install
```

**Step 2:** Signup (if not done already) and [create an OpenAI API key](https://platform.openai.com/api-keys).

**Step 3:** Export environment variables:

```bash
export OPENAI_CODE_ASSIST_KEY=YOUR_OPENAI_API_KEY_CREATED_ABOVE
export AIDER_MODEL="o3-mini" # or "gpt-4.1" etc.
```

**Step 4:** Create an alias to invoke aider:

```bash
alias copilot="OPENAI_API_KEY=$OPENAI_CODE_ASSIST_KEY aider --model $AIDER_MODEL"
```

> You can add the above exports and alias in your shell's environment file, e.g. `~/.zshrc`

</details>
</details>


## Project Setup

> Following is a one time setup required when you first clone the project and install dependencies and configurations...

<details>
<summary>Initialize project</summary>

**Step 1:** clone the repo and create a python virtual environment within the repo project directory:

```bash
git clone https://github.com/gnulib/demo-adk-app.git

cd demo-adk-app

python3 -m venv .venv
```

**Step 2:** initialize environment to work in project

```bash
source .venv/bin/activate
```

</details>

<details>

<summary>Install dependencies</summary>

_Install backend project dependencies:_

```bash
pip install -r backend/requirements.txt
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

_In another terminal run the ADK app locally for testing project setup_

```bash
# option 1 to use CLI
(cd backend; adk run simple_agent)

# option 2 to use web interface
(cd backend; adk web)
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
gcloud run services describe "$GOOGLE_ADK_APP_NAME-service" --platform managed --region $GOOGLE_CLOUD_LOCATION
```

</details>

<details>

<summary>Interact with ADK app</summary>

> Use the service URL from above, or use `gcloud run services describe "$GOOGLE_ADK_APP_NAME-service" --platform managed --region $GOOGLE_CLOUD_LOCATION --format='value(status.url)'`

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
