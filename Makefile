# Makefile for building the application components

# Check for required environment variables for the backend build
ifndef GOOGLE_CLOUD_LOCATION
 $(error GOOGLE_CLOUD_LOCATION is not set. Please set this environment variable.)
endif
ifndef GOOGLE_ADK_APP_REPOSITORY
 $(error GOOGLE_ADK_APP_REPOSITORY is not set. Please set this environment variable.)
endif
ifndef GOOGLE_ADK_APP_NAME
 $(error GOOGLE_ADK_APP_NAME is not set. Please set this environment variable.)
endif
# Check for GOOGLE_GENAI_USE_VERTEXAI, default to false if not set
ifndef GOOGLE_GENAI_USE_VERTEXAI
    $(warning WARNING: GOOGLE_GENAI_USE_VERTEXAI is not set. Defaulting to 'false'.)
    GOOGLE_GENAI_USE_VERTEXAI := false
endif
ifndef FIREBASE_APP_URL
    $(warning WARNING: FIREBASE_APP_URL is not set. Defaulting to 'https://default-firebase-app.web.app'.)
    FIREBASE_APP_URL := "https://default-firebase-app.web.app"
endif

.PHONY: deploy-backend verify-backend

# Target to build and deploy the backend using Google Cloud Build
deploy-backend:
	@echo "Building and deploying backend using Cloud Build..."
	@(cd backend; gcloud builds submit --config=cloudbuild.yaml . --substitutions="_AR_REGION=$(GOOGLE_CLOUD_LOCATION),_AR_REPO_NAME=$(GOOGLE_ADK_APP_REPOSITORY),_APP_NAME=$(GOOGLE_ADK_APP_NAME),_GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI),_FIREBASE_APP_URL=$(FIREBASE_APP_URL)")

# Target to verify the status of the deployed backend service
verify-backend:
	@echo "Verifying backend deployment status..."
	@gcloud run services describe "$(GOOGLE_ADK_APP_NAME)-service" --platform managed --region $(GOOGLE_CLOUD_LOCATION)

# Example placeholder for a frontend build target
# .PHONY: build-frontend
# build-frontend:
#	@echo "Building frontend..."
#	@(cd frontend; npm install && npm run build)

# Example placeholder for a clean target
# .PHONY: clean
# clean:
#	@echo "Cleaning up..."
#	# Add commands to clean build artifacts if necessary
