## Firebase Setup

> You'll be required to have a firebase project linked to the google cloud project created for this demo, as following...

### Install Firebase tooling

<details>

<summary><b>Step 1:</b> Install <code>Node</code> <i>(if not already have it)</i></summary>

 > Install [Node.js](https://www.nodejs.org/) using [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) on your development machine:

_(first install nvm)_
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

_(second, close and reopen new terminal window)_

_(third, install node v22.x using nvm)_

```bash
nvm install 22
````

_(Installing Node.js automatically installs the `npm` command tools)_

</details>

<details>

<summary><b>Step 2:</b> Install Firebase CLI <i>(if not already have it)</i></summary>

```bash
npm install -g firebase-tools
```
</details>

<details>

<summary><b>Step 3:</b> Authorize Firebase CLI for your project</summary>

> (optional) if you are already logged in from a different / work account, then logout:

```bash
firebase logout
```

> authenticate and authorize firebase CLI with same Google account that the GCP project is linked with:

```bash
(source .env; firebase login)
```

> Above command will open a browser window asking you to log in with your Google account and grant Firebase CLI the necessary permissions. Once you've successfully logged in, the terminal will confirm that you are authenticated.

</details>

<details>

<summary><b>Step 4:</b> Add firebase to your google cloud project</summary>

> Make sure you have completed the [GCP Setup](GCP_SETUP.md) steps already!

```bash
(source .env; cd frontend/; firebase projects:addfirebase $GOOGLE_CLOUD_PROJECT)
```

> If you already had firebase added to google cloud project, then might get error, you can ignore that.

</details>

> Configure `firebase` to use your google project for frontend:

```bash
(source .env; cd frontend; firebase use --add $GOOGLE_CLOUD_PROJECT)
```

<details>

<summary><b>Step 5:</b> Enable email/password authentication for your firebase project</summary>

1. Go to the [Firebase console](https://console.firebase.google.com/)

1. Select your project created above.

1. On project dashboard, under Build -> Authentication click on “Get started”

1. Select sign-in method, click on Add new provider

1. Select the Native provider “Email/Password”, toggle “Enable” to on, save

</details>

<details>

<summary><b>Step 6:</b> Disable user self creation</summary>

1. Goto “Settings” tab under Authentication

1. Click on “User actions”

1. Deselect “Enable create” checkbox

1. Save

</details>

### Initialize Firebase for Your Project

<details>

<summary><b>Step 1:</b> Initialize hosting for your frontend</summary>

```bash
(source .env; cd frontend; firebase init hosting --project $GOOGLE_CLOUD_PROJECT)
```

This command will start an interactive process. Here's how to respond to the prompts:

1. **What do you want to use as your public directory?** This is the most important step for a React app. The build process for React applications (using `create-react-app`) typically outputs the production files into a `build` or `dist` folder. Enter `build` (or `dist` if you are using Vite or a custom setup) and press Enter.

1. **Configure as a single-page application (rewrite all urls to /index.html)?** Type `Yes` (`y`) and press Enter. This is crucial for single-page applications like React apps, ensuring that routing works correctly.

1. **Set up automatic builds and deploys with GitHub?** Type `No` (`n`) unless you specifically want to set up continuous deployment with GitHub Actions at this time. You can always set this up later.

1. **File build/index.html already exists. Overwrite?** Type `No` (`n`). You don't want to overwrite the `index.html` file that is generated during the build process.

After completing these steps, Firebase will create two new files in your project's root directory: `.firebaserc` and `firebase.json`.

* `.firebaserc`: Stores your default Firebase project alias.

* `firebase.json`: Contains the configuration for Firebase services, including Hosting. It will specify your public directory (`build`) and the rewrite rule for single-page applications.

</details>

<details>

<summary><b>Step 2:</b> Create test user for project</summary>

1. Go to the [Firebase console](https://console.firebase.google.com/)

1. Select your project created above.

1. On project dashboard, under Build -> Authentication click on “Users” tab

1. Click on "Add user"

1. Enter email and password for a test user (e.g. `test@example.com` / `secret123`)

> The above test user can have any email/password, save it for using with testing later.

</details>

<details>

<summary><b>Step 3:</b> Create a new web app for your firebase project</summary>

> _(first confirm that you don't already have web app)_

```bash
(source .env; cd frontend; firebase apps:list)
```

> _(if don't have web app already, then create new)_

```bash
(source .env; cd frontend; firebase apps:create web)
```

This command will start an interactive process. Here's how to respond to the prompts:

1. **What would you like to call your app?** Use "demo-adk-app-frontend".

> save the app ID from output for use below.

</details>

<details>

<summary><b>Step 4:</b> Export environment variables related to Firebase project</summary>

> update the `.env` file in project's root directory with firebase web app ID and URLs:

```bash
cat >> .env <<'EOF'
# Firebase Project specific environment variables
export FIREBASE_APP_ID=<<app ID from above>>
export FIREBASE_APP_URLS="https://$GOOGLE_CLOUD_PROJECT.web.app"

EOF
```

</details>

### Setup firebase frontend environment

<details>

<summary><b>Step 1:</b> Copy <code>frontend/.env.example</code> file as <code>frontend/.env</code></summary>

```bash
cp frontend/.env.example frontend/.env
```
</details>

<details>

<summary><b>Step 2:</b> Get firebase web app configuration</summary>

```bash
(source .env; cd frontend; firebase apps:sdkconfig WEB $FIREBASE_APP_ID)
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

</details>

<details>

<summary><b>Step 3:</b> replace the placeholder values in <code>frontend/.env</code></summary>

> Use the actual actual configuration from previous step to update values in `frontend/.env`.

> **Important**: Keep your apiKey and other configuration details secure. While the apiKey for web apps is generally considered safe to include in your client-side code (as it only allows access to services you've enabled and configured security rules for), you should never expose sensitive server-side keys.

</details>
