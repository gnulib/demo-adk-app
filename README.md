# demo-adk-app

_(This project is intentionally designed as a monorepo, i.e., has both the frontend and backend code in the same git repository. For a larger, more complex, or production-grade applications, separating frontends and backends into different repositories is often recommended for better team collaboration, independent scaling, and clearer separation of concerns.)_

> **Acknowledgement:**  
> This project makes use of the excellent [Deck of Cards API](https://deckofcardsapi.com/) by Chase Roberts. Many thanks to Chase for providing this fun and useful API!

## Blog Series Companion
This repository serves as a hands-on companion for a 3-part blog series.
*   **Part 2:** [The Agent Stack : Hosting a Secure Agent App with Firebase and Cloud Run](https://www.linkedin.com/pulse/agent-stack-hosting-secure-app-firebase-cloud-run-amit-bhadoria-cjvuc) - is now live!
*   To follow the hands-on exercises for Part 2, please check out the specific code state using the following git command:
     ```bash
     git checkout tags/blog-part-2
     ```
> This command creates a new detached copy of project code from the `blog-part-2` tag, allowing you to work through the exercises.

## Developer Setup

> Following is a one time developer setup required on top of setup done with earlier parts of the blog series...
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

**Step 2:** Enable the Identity Toolkit APIs in your project:

```bash
gcloud services enable identitytoolkit.googleapis.com aiplatform.reasoningEngines.list
```
> Above is new API for firebase authentication introduced in this part of the blog series, in addition to other APIs that were enabled in the earlier parts of the blog series.

**Step 3:** Create a Cloud Storage bucket for your project (used for RAG and Agent Engine ID):

```bash
gcloud storage buckets create gs://$GOOGLE_ADK_APP_NAME-$GOOGLE_CLOUD_PROJECT \
    --default-storage-class STANDARD \
    --location $GOOGLE_CLOUD_LOCATION
```

_(If you already have the bucket created earlier, you may get below error and you can ignore it:)_

> ERROR: (gcloud.storage.buckets.create) HTTPError 409: Your previous request to create the named bucket succeeded and you already own it.

**Step 4:** Add necessary roles to service account:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/run.admin \
  --condition=None

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/cloudbuild.builds.builder \
  --condition=None

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/iam.serviceAccountUser \
  --condition=None

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/aiplatform.admin \
  --condition=None
  ```

**Step 5:** Add necessary secret key access to service account:

```bash
# No secret key access to be added yet.
```

**Step 6:** (optional) override default organization policy `iam.allowedPolicyMemberDomains`
* if your google project is part of an organization (e.g. associated with a google workspace) then it will inherit parent organization's policy `iam.allowedPolicyMemberDomains`, which prevents allowing all users access to cloud run service deployed in the project
* need to override this at the project level as following:
  * browse to cloud console -> IAM -> Organization policy
  * search for `iam.allowedPolicyMemberDomains`, click details
  * from policy detail page, click on "Manage policy"
  * under "Policy Source", select "Override parent's policy"
  * under "Polocy enforcement", select "Replace"
  * under "Rules", add rule with value "Allow All"
  * click Done
  * click "Set polocy"
* verify that project has the override configured / enabled:

```bash
gcloud org-policies list --project=$GOOGLE_CLOUD_PROJECT_ID
```


**Step 6:** Verify your configurations:

```bash
gcloud config list # verify gcloud is using correct google cloud account and project

gcloud artifacts repositories list # verify artifact repository exists

gcloud storage buckets list --format="json(name)" # verify that storage bucket for app name exists
```

> Above command will display your current `gcloud` configuration, including the active account and the project, and the default region/zone if you set them. These should match the project and google cloud account you are using for this demo.

</details>

<details>
<summary>Firebase Setup</summary>

> You'll be required to have a firebase project linked to the google cloud project created above, as following...

**Step 1:** Install [Node.js](https://www.nodejs.org/) using [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) on your development machine:

_(first install nvm)_
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

_(second, close and reopen new terminal window)_

_(third, install node using nvm)_

```bash
nvm install node
````

_(Installing Node.js automatically installs the `npm` command tools)_

**Step 2:** Install firebase CLI on your development machine:

```bash
npm install -g firebase-tools
```

**Step 3:** Log in to firebase with your CLI:

```bash
# use 'firebase logout' if you are already logged in from a
# different / work account and need to switch to personal account
firebase login
```

>This command will open a browser window asking you to log in with your Google account and grant Firebase CLI the necessary permissions. Once you've successfully logged in, the terminal will confirm that you are authenticated.

**Step 4:** Add firebase to your google cloud project:

```bash
firebase projects:addfirebase $GOOGLE_CLOUD_PROJECT
```

> If you already had firebase added to google cloud project, then might get error, you can ignore that.


**Step 5:** Enable email/password authentication for your firebase project:

1. Go to the [Firebase console](https://console.firebase.google.com/)

1. Select your project created above.

1. On project dashboard, under Build -> Authentication click on “Get started”

1. Select sign-in method, click on Add new provider

1. Select the Native provider “Email/Password”, toggle “Enable” to on, save

**Step 6:** Disable user self creation:
1. Goto “Settings” tab under Authentication

1. Click on “User actions”

1. Deselect “Enable create” checkbox

1. Save

</details>

## Project Setup

> Following is a one time setup required on top of setup done with Part - 1 of the blog series. If you have not completed the previous parts, please complete them before continuing here.

<details>

<summary>Install dependencies</summary>

> Activate project's virtual environment:

```bash
source .venv/bin/activate
```

> Install core development tools for project:

```bash
# only required first time
pip install --upgrade pip setuptools wheel build twine pip-tools
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

<summary>Initialize Firebase for Your Project</summary>

**Step 1:** Configure `firebase` to use your google project for frontend:

```bash
(cd frontend; firebase use $GOOGLE_CLOUD_PROJECT)
```

**Step 2:** Initialize hosting for your frontend:

```bash
(cd frontend; firebase init hosting)
```

This command will start an interactive process. Here's how to respond to the prompts:

1. **What do you want to use as your public directory?** This is the most important step for a React app. The build process for React applications (using `create-react-app`) typically outputs the production files into a `build` or `dist` folder. Enter `build` (or `dist` if you are using Vite or a custom setup) and press Enter.

1. **Configure as a single-page application (rewrite all urls to /index.html)?** Type `Yes` (`y`) and press Enter. This is crucial for single-page applications like React apps, ensuring that routing works correctly.

1. **Set up automatic builds and deploys with GitHub?** Type `No` (`n`) unless you specifically want to set up continuous deployment with GitHub Actions at this time. You can always set this up later.

1. **File build/index.html already exists. Overwrite?** Type `No` (`n`). You don't want to overwrite the `index.html` file that is generated during the build process.

After completing these steps, Firebase will create two new files in your project's root directory: `.firebaserc` and `firebase.json`.

* `.firebaserc`: Stores your default Firebase project alias.

* `firebase.json`: Contains the configuration for Firebase services, including Hosting. It will specify your public directory (`build`) and the rewrite rule for single-page applications.

**Step 3:** Create test user for project:

1. Go to the [Firebase console](https://console.firebase.google.com/)

1. Select your project created above.

1. On project dashboard, under Build -> Authentication click on “Users” tab

1. Click on "Add user"

1. Enter email and password for a test user (e.g. `test@example.com` / `secret123`)

> The above test user can have any email/password, save it for using with testing later.

**Step 4:** Create a new web app for your firebase project:

_(first confirm that you don't already have web app)_

```bash
(cd frontend; firebase apps:list)
```

_(if don't have web app already, then create new)_

```bash
(cd frontend; firebase apps:create web)
```

This command will start an interactive process. Here's how to respond to the prompts:

1. **What would you like to call your app?** Use "demo-adk-app-frontend".

> save the app ID from output for use below.

**Step 5:** Store the firebase web app ID and URLs as environment variable:

```bash
export FIREBASE_APP_ID=<<app ID from above>>
export FIREBASE_APP_URLS="https://$GOOGLE_CLOUD_PROJECT.web.app"
```

>TIP: you can add above line to your shell's rc file, e.g. `~/.zshrc` and reload

</details>

<details>

<summary>Setup firebase frontend environment</summary>

**Step 1:** Copy `frontend/.env.example` file as `frontend/.env`

```bash
cp frontend/.env.example frontend/.env
```

**Step 2:** Get firebase web app configuration:

```bash
(cd frontend; firebase apps:sdkconfig WEB $FIREBASE_APP_ID)
```

> output will look something like below:

```js
{
  projectId: "YOUR_FIREBASE_PROJECT_ID",
  appId: "YOUR_FIREBASE_APP_ID",
  storageBucket: "YOUR_FIREBASE_STORAGE_BUCKET",
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "YOUR_FIREBASE_AUTH_DOMAIN",
  messagingSenderId: "YOUR_FIREBASE_MESSAGING_SENDER_ID"
}
```

**Step 3:** replace the placeholder values in `frontend/.env` file with your actual configuration from above.

> **Important**: Keep your apiKey and other configuration details secure. While the apiKey for web apps is generally considered safe to include in your client-side code (as it only allows access to services you've enabled and configured security rules for), you should never expose sensitive server-side keys.

</details>

<details>

<summary>Setup backend environment</summary>

_create `backend/.env` file for local testing:_

```bash
cat > backend/.env <<'EOF'
export GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT
export GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION
export GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI
export APP_NAME=$GOOGLE_ADK_APP_NAME
export PORT=8000
export CORS_ORIGINS="http://localhost:3000, $FIREBASE_APP_URLS"
export IS_TESTING=true
export DECKOFCARDS_URL="https://deckofcardsapi.com/api/deck"
EOF
```

</details>

## Getting Started
> You'll be using two terminals, one terminal will be used to run backend service, and another terminal will be where you'll be running the frontend app for local testing.

<details>
<summary>Test backend setup locally</summary>

_In one terminal run the app locally for testing project setup_

```bash
(source backend/.env; cd backend/src; uvicorn demo_adk_app.main:app --reload)
```

_In another terminal run the test CLI for interacting with the app (use port from above)_

```bash
(export $(grep REACT_APP_FIREBASE_API_KEY frontend/.env); cd backend; python test/cli.py --port 8000)

cli> help

cli> lc # this command lists existing conversations

cli> cc # this command creates a new conversation

cli> join <<conversation id>> # this command joins a conversation
```

> When you interact with the agent, if you get error like `google.genai.errors.ClientError: 403 PERMISSION_DENIED` -- this usually means either VertexAI API has not be enabled in your project, or your current environment is using a different google cloud project. Please make sure that you have completed all the steps mentioned above in "Google Cloud Setup" and are using the correct google project in your environment variables (`GOOGLE_CLOUD_PROJECT`) and with `gcloud` CLI _(check config in `gcloud config list` and `gcloud auth list`)_.

</details>

<details>

<summary>Test frontend setup locally</summary>

1. _Once backend looks good, start frontend to interact with local agent service:_

```bash
(cd frontend; npm run start)
```
> _(above command uses `REACT_APP_BACKEND_URL` from `frontend/.env` file, and assumption is that local backend is running and listening on the same port mentioned in that variable. If port is different then modify the entry in `frontend/.env` file accordingly)_

1. _(make sure that you have test user created as mentioned in project setup above)_

1. _Interact with the app frontend and confirm connectivity and functionality works as expected._


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
