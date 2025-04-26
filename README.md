# demo-adk-app

This is a demo project for a simple app using [Google's ADK](https://google.github.io/adk-docs/) framework. This project is intended to demonstrate the following:

* how to setup a GCP project for deploying ADK app as a cloud run service
* how to use a react front end client hosted on firebase as static site to interact with ADK app via APIs
* how to use firebase authentication with ADK app

Secondary objective of this project is to demonstrate the power of LLMs, how they can be used to build conversation interface against pretty much any service that has reasonable APIs.

> This project is intentionally designed as a monorepo, i.e., has both the frontend and backend code in the same git repository. For a larger, more complex, or production-grade applications, separating frontends and backends into different repositories is often recommended for better team collaboration, independent scaling, and clearer separation of concerns.

## Developer Setup

> Following is a one time developer setup required to install appropriate tools and configurations on local machine, and to get Google Cloud resources created...

<details>
<summary>Google Cloud Setup</summary>

**Step 1:** Create a new [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and enable billing.

> If you are an individual developer, you should be able to signup for a new Google Cloud by [getting started for free](https://cloud.google.com/free) program.

**Step 2:** Install [gcloud](https://cloud.google.com/sdk/docs/install) on your local development machine and initialize gcloud to use the new project created above

> If you already have gcloud installed / configured from your work account, then you might want to create a new configuration (in addition to existing work configuration) with `gcloud init` using your personal google cloud account.

</details>

<details>
<summary>Firebase Setup</summary>

**Step 1:** Create a new [Firebase project](https://firebase.google.com/docs/web/setup#create-project) to link with Google Cloud project created above

> Use the option to "Add Firebase to an existing Google Cloud project" (at the bottom of page).

**Step 2:** [Register your app](https://firebase.google.com/docs/web/setup#register-app) with your new firebase project created above.

> For simplicity, we'll use Web platform for creating new app.

**Step 3:** Install firebase on your local development machine:

```bash
npm install firebase
```

</details>

<details>
<summary>aider Setup</summary>

<details>
<summary> Option 1: aider with Vertex AI gemini model</summary>

**Step 1:** Install [aider](https://aider.chat/):

```bash
python -m pip install aider-install

aider-install
```

**Step 2:** Export environment variables (in this example we'll use VertexAI APIs with aider):

```bash
export GOOGLE_CLOUD_PROJECT=YOUR_GOOGLE_PROJECT_CREATED_ABOVE
export GOOGLE_CLOUD_LOCATION=LOCATION_TO_USE #e.g. us-central1
export GOOGLE_GENAI_USE_VERTEXAI="True"
export VERTEXAI_PROJECT=$GOOGLE_CLOUD_PROJECT
export VERTEXAI_LOCATION=$GOOGLE_CLOUD_LOCATION
export AIDER_MODEL="vertex_ai/gemini-2.5-pro-exp-03-25" # (this one is free because it's experimental)
```

> You can add the above exports into your shell's environment file, e.g. `~/.zshenv`

**Step 3:** Make sure you have authenticated against the project:

```bash
gcloud auth application-default login
```

**Step 4:** (Optional) create an alias to invoke aider:

```bash
alias copilot="aider --model $AIDER_MODEL"
```
</details>
<details>
<summary>Option 2: aider with OpenAI gpt model</summary>

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

> You can add the above exports into your shell's environment file, e.g. `~/.zshenv`

**Step 4:** (Optional) create an alias to invoke aider:

```bash
alias copilot="OPENAI_API_KEY=$OPENAI_CODE_ASSIST_KEY aider --model $AIDER_MODEL"
```

</details>
</details>


## Getting Started

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

**Step 3:** install backend project dependencies
```bash
pip install -r backend/requirements.txt
```

</details>
