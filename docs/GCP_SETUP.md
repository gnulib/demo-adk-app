## GCP Setup

> You'll be required to have a Google Cloud project, either in your own personal account, or your enterprise / work related account, as following ...

<details>

<summary><b>Step 1:</b> Create a new <a href="https://cloud.google.com/resource-manager/docs/creating-managing-projects"> Google Cloud project </a> and enable billing.</summary>


> If you are an individual developer, you should be able to signup for a new Google Cloud by [getting started for free](https://cloud.google.com/free) program.

</details>

<details>

<summary><b>Step 2:</b> Install and setup <a href="https://cloud.google.com/sdk/docs/install">gcloud</a> on your local development machine </summary>

> If you already have gcloud installed / configured from your work account and you want to use this example project with your personal account, then you might want to create a new configuration (in addition to existing work configuration) with `gcloud init` using your personal google cloud account.

</details>

<details>

<summary><b>Step 3:</b> Export environment variables related to project</summary>

> below `.env` file should be at the root of your project directory and sourced every time you start working on the project in a new terminal session.

```bash
cat > .env <<'EOF'
export GOOGLE_CLOUD_PROJECT="<<<YOUR_GOOGLE_PROJECT_CREATED_ABOVE>>>"
export GOOGLE_CLOUD_LOCATION="<<<<LOCATION_TO_USE>>>" #e.g. us-central1
export GOOGLE_CLOUD_PROJECT_NUMBER="$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format='value(projectNumber)')"
export GOOGLE_ADK_APP_REPOSITORY="adk-apps"
export GOOGLE_ADK_APP_NAME="demo-adk-app"
export GOOGLE_GENAI_USE_VERTEXAI="True"
export PORT=8000
export CORS_ORIGINS="http://localhost:3000, $FIREBASE_APP_URLS"
export IS_TESTING=true
export DECKOFCARDS_URL="https://deckofcardsapi.com/api/deck"
EOF
```

> source the `.env` in your current terminal session for susequent steps

```bash
source .env
```
</details>

<details>

<summary><b>Step 4:</b> Setup <code>gcloud</code> for your GCP project</summary>

> Setup your default Google Cloud project for subsequent steps

```bash
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

> Generate a local Application Default Credentials (ADC) file using Google account that is associated with the GCP project.

```bash
gcloud auth application-default login
```
</details>

<details>

<summary><b>Step 5:</b> Enable the APIs for your GCP project</summary>

> GCP project need to have following APIs enabled:
> * Cloud Build
> * Cloud Run
> * Artifact Registry
> * Identity Toolkit
> * VertexAI APIs

```bash
gcloud services enable \
cloudbuild.googleapis.com \
run.googleapis.com \
artifactregistry.googleapis.com \
identitytoolkit.googleapis.com \
aiplatform.googleapis.com
```
</details>

<details>

<summary><b>Step 6:</b> Create a repository in Artifact Registry to store your ADK app images</summary>

> If you already have repository created earlier then you might get an error message that can be ignored.

```bash
gcloud artifacts repositories create $GOOGLE_ADK_APP_REPOSITORY \
--repository-format=docker --location=$GOOGLE_CLOUD_LOCATION \
--description="ADK applications container repository"
```

</details>

<details>

<summary><b>Step 7:</b> Create a Cloud Storage bucket for your project </summary>

> GCP project needs a GCS bucket to use for RAG and Agent Engine ID setup:

```bash
gcloud storage buckets create gs://$GOOGLE_ADK_APP_NAME-$GOOGLE_CLOUD_PROJECT \
    --default-storage-class STANDARD \
    --location $GOOGLE_CLOUD_LOCATION
```

_(If you already have the bucket created earlier, you may get below error and you can ignore it:)_

> ERROR: (gcloud.storage.buckets.create) HTTPError 409: Your previous request to create the named bucket succeeded and you already own it.

</details>

<details>

<summary><b>Step 8:</b> Add necessary roles to service account</summary>

> add `run.admin` role:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/run.admin \
  --condition=None
```

> add `cloudbuild.builds.builder` role:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/cloudbuild.builds.builder \
  --condition=None
```

> add `iam.serviceAccountUser` role:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/iam.serviceAccountUser \
  --condition=None
```

> add `aiplatform.admin` role:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member=serviceAccount:$GOOGLE_CLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/aiplatform.admin \
  --condition=None
  ```

</details>

<details>
<summary><b>Step 9:</b> (optional) override default organization policy</summary>

> if your google project is part of an organization (e.g. associated with a google workspace) then it will inherit parent organization's policy which prevents allowing all users access to cloud run service deployed in the project.

* check if google project is part of an organization:

```bash
gcloud organizations list
```

> above command lists organizations (if applicable) with ORG ID

* check for org policy `iam.allowedPolicyMemberDomains` (if an org was listed above):

```bash
gcloud org-policies list --organization=<<ORG_ID>>
```

> if your org has restrictions, then you'll see something like below:
> ```
> iam.allowedPolicyMemberDomains                      SET          -               CN65xb8GEKjRvMMD-
> ```

* override `iam.allowedPolicyMemberDomains` _(if it was enabled for org)_ at the project level by requesting your org admin following:
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
gcloud org-policies list --project=$GOOGLE_CLOUD_PROJECT
```
</details>


### Verify your configurations

_(below commands will display your current `gcloud` configurations, including the active account and the project, and the default region/zone if you set them. These should match the project and google cloud account you are using for this demo.)_

> verify gcloud is using correct google cloud account and project:

```bash
gcloud config list
```

> verify artifact repository exists:
```bash
gcloud artifacts repositories list
```

> verify that storage buckets for app name exists:

```bash
gcloud storage buckets list --format="json(name)"
```

