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

.PHONY: build-backend

# Target to build the backend using Google Cloud Build
build-backend:
	@echo "Building backend using Cloud Build..."
	@(cd backend; gcloud builds submit --config=cloudbuild.yaml . --substitutions="_AR_REGION=$(GOOGLE_CLOUD_LOCATION),_AR_REPO_NAME=$(GOOGLE_ADK_APP_REPOSITORY),_APP_NAME=$(GOOGLE_ADK_APP_NAME),_GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI)")

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
