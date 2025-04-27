# demo-adk-app

> **Acknowledgement:**  
> This project makes use of the excellent [Deck of Cards API](https://deckofcardsapi.com/) by Chase Roberts. Many thanks to Chase for providing this fun and useful API!

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

> You'll be required to have a Google Cloud project, either in your own personal account, or your enterprise / work related account, as following ...

**Step 1:** Create a new [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and enable billing.

> If you are an individual developer, you should be able to signup for a new Google Cloud by [getting started for free](https://cloud.google.com/free) program.

**Step 2:** Install [gcloud](https://cloud.google.com/sdk/docs/install) on your local development machine and initialize gcloud to use the new project created above

> If you already have gcloud installed / configured from your work account and you want to following this example project in your personal account, then you might want to create a new configuration (in addition to existing work configuration) with `gcloud init` using your personal google cloud account.

**Step3:** Generate a local Application Default Credentials (ADC) file to be used by ADK app for VertexAI API calls:

```bash
gcloud auth application-default login
```

**Step 4:** Verify your configuration:

```bash
gcloud config list
```

> This command will display your current `gcloud` configuration, including the active account and the project, and the default region/zone if you set them. These should match the project and google cloud account you are using for this demo.

**Step 5:** Export environment variables related to project:

```bash
export GOOGLE_CLOUD_PROJECT=YOUR_GOOGLE_PROJECT_CREATED_ABOVE # gcloud config get-value project
export GOOGLE_CLOUD_LOCATION=LOCATION_TO_USE #e.g. us-central1
export GOOGLE_GENAI_USE_VERTEXAI="True"
```

> You can add the above exports into your shell's environment file, e.g. `~/.zshenv`

</details>

<details>

<summary>VertexAI API Setup</summary>

> You need to enable the VertexAI API for your google cloud project created above as following...

**Step 1:** Log into google cloud [API & Services console](https://console.cloud.google.com/apis/dashboard).

**Step 2:** Make sure you have the correct google project selected from project selection drop down on top.

> Shortcut URL to your project specific dashboard is `https://console.cloud.google.com/apis/dashboard?project=YOUR_GOOGLE_CLOUD_PROJECT`

**Step 3:** Click on "+ Enable APIs and services".

**Step 4:** Search for `Vertex AI API`, click on result

**Step 5:** Enable the API.

</details>

<details>
<summary>Firebase Setup</summary>

> You'll be required to have a firebase project linked to the google cloud project created above, as following...

**Step 1:** Create a new [Firebase project](https://firebase.google.com/docs/web/setup#create-project) to link with Google Cloud project created above

> Use the option to "Add Firebase to an existing Google Cloud project" (at the bottom of page).

**Step 2:** [Register your app](https://firebase.google.com/docs/web/setup#register-app) with your new firebase project created above.

> For simplicity, we'll use Web platform for creating new app.

**Step 3:** Enable [email link sign-in](https://firebase.google.com/docs/auth/web/email-link-auth#enable_email_link_sign-in_for_your_firebase_project) for your firebase project.

> Authentication section is under project Dashboard -> Build -> Authentication.

**Step 4:** Install firebase CLI on your local development machine:

```bash
npm install -g firebase-tools
```

**Step 5:** Log in to firebase with your CLI:

```bash
# use 'firebase logout' if you are already logged in from a
# different / work account and need to switch to personal account
firebase login
```

>This command will open a browser window asking you to log in with your Google account and grant Firebase CLI the necessary permissions. Once you've successfully logged in, the terminal will confirm that you are authenticated.

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

> You can add the above exports into your shell's environment file, e.g. `~/.zshenv`

**Step 4:** (Optional) create an alias to invoke aider:

```bash
alias copilot="OPENAI_API_KEY=$OPENAI_CODE_ASSIST_KEY aider --model $AIDER_MODEL"
```

</details>
</details>


## Getting Started

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

**Step 1:** install backend project dependencies

```bash
pip install -r backend/requirements.txt
```

**Step 2:** install frontend project dependencies

```bash
cd frontend

npm install

cd ..
```
</details>

<details>

<summary>Update Firebase configurations</summary>

**Step 1:** Copy `frontend/.env.example` file as `frontend/.env`

```bash
cp frontend/.env.example frontend/.env
```

**Step 2:** Go to the [Firebase console](https://console.firebase.google.com/).

**Step 3:** Select your project.

**Step 4:** Click on the "Project settings" gear icon (usually near the top left).

**Step 5:** Scroll down to the "Your apps" section.

**Step 6:** Click on the web app you registered.

**Step 7:** You will see a section titled "Firebase SDK snippet". Choose the "Config" option.

> It will look something like below:

```js
const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "YOUR_FIREBASE_AUTH_DOMAIN",
  projectId: "YOUR_FIREBASE_PROJECT_ID",
  storageBucket: "YOUR_FIREBASE_STORAGE_BUCKET",
  messagingSenderId: "YOUR_FIREBASE_MESSAGING_SENDER_ID",
  appId: "YOUR_FIREBASE_APP_ID",
  measurementId: "YOUR_FIREBASE_MEASUREMENT_ID" // Optional
};
```

**Step 8:** replace the placeholder values in `frontend/.env` file with your actual configuration from above.

> **Important**: Keep your apiKey and other configuration details secure. While the apiKey for web apps is generally considered safe to include in your client-side code (as it only allows access to services you've enabled and configured security rules for), you should never expose sensitive server-side keys.

</details>

<details>

<summary>Initialize Firebase Hosting for Your Project</summary>

Run the Firebase initialization command:

```bash
(cd frontend; firebase init)
```

This command will start an interactive process. Here's how to respond to the prompts:

1. **Which Firebase features do you want to set up for this directory?** Use the spacebar to select `Hosting: Configure files for Firebase Hosting and (optionally) set up GitHub Action deploys` and press Enter.

1. **Select a default Firebase project for this directory:** Choose the Firebase project you created for this application from the list.

1. **What do you want to use as your public directory?** This is the most important step for a React app. The build process for React applications (using `create-react-app`) typically outputs the production files into a `build` or `dist` folder. Enter `build` (or `dist` if you are using Vite or a custom setup) and press Enter.

1. **Configure as a single-page application (rewrite all urls to /index.html)?** Type `Yes` (`y`) and press Enter. This is crucial for single-page applications like React apps, ensuring that routing works correctly.

1. **Set up automatic builds and deploys with GitHub?** Type `No` (`n`) unless you specifically want to set up continuous deployment with GitHub Actions at this time. You can always set this up later.

1. **File build/index.html already exists. Overwrite?** Type `No` (`n`). You don't want to overwrite the `index.html` file that is generated during the build process.

After completing these steps, Firebase will create two new files in your project's root directory: `.firebaserc` and `firebase.json`.

* `.firebaserc`: Stores your default Firebase project alias.

* `firebase.json`: Contains the configuration for Firebase services, including Hosting. It will specify your public directory (`build`) and the rewrite rule for single-page applications.

</details>

> You'll be using two terminals, besides any IDE you might be using to view / navigate project files. One terminal will be used to run `aider` for any copilot help (e.g., asking to help describe code), and another terminal will be where you'll be running the frontend / backend apps for local testing.


**Step 1:** start aider on terminal _(assuming you configured alias in aider setup above)_

```bash
copilot
```

> This documentation assumes you are using aider on a terminal window as a copilot for learning about project, or making changes to project as per your needs.

**Step 2:** run the ADK app locally for testing

```bash
# option 1 to use CLI
(cd backend; adk run simple_agent)

# option 2 to use web interface
(cd backend; adk web)
```

> When you interact with the agent, if you get error like `google.genai.errors.ClientError: 403 PERMISSION_DENIED` -- this usually means either VertexAI API has not be enabled in your project, or your current environment is using a different google cloud project. Please make sure that you have completed all the steps mentioned above in "Google Cloud Setup" and "VertextAI API Setup" and are using the correct google project in your environment variables (`GOOGLE_CLOUD_PROJECT`) and with `gcloud` CLI _(check config in `gcloud config list` and `gcloud auth list`)_.

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
