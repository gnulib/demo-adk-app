# demo-adk-app

This is a demo project for a simple app using [Google's ADK](https://google.github.io/adk-docs/) framework. This project is intended to demonstrate the following:

* how to setup a GCP project for deploying ADK app as a cloud run service
* how to use a react front end client hosted on firebase as static site to interact with ADK app via APIs
* how to use firebase authentication with ADK app

Secondary objective of this project is to demonstrate the power of LLMs, how they can be used to build conversation interface against pretty much any service that has reasonable APIs.

> This project is intentionally designed as a monorepo, i.e., has both the frontend and backend code in the same git repository. For a larger, more complex, or production-grade applications, separating frontends and backends into different repositories is often recommended for better team collaboration, independent scaling, and clearer separation of concerns.

## Developer Setup

Step 1: Create a new [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and enable billing.

> If you are an individual developer, you should be able to signup for a new Google Cloud by [getting started for free](https://cloud.google.com/free) program.

Step 2: Create a new [Firebase project](https://firebase.google.com/docs/web/setup#create-project) using the option to "Add Firebase" to an existing Google Cloud project, created above.

Step 3: [Register your app](https://firebase.google.com/docs/web/setup#register-app) with your new firebase project created above

Step 3: Install [gcloud](https://cloud.google.com/sdk/docs/install) on your local development machine and initialize gcloud to use the new project created above

Step 4: Install firebase on your local development machine.

```bash
npm install firebase
```
