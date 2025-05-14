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
    FIREBASE_APP_URL := https://default-firebase-app.web.app
endif

.PHONY: deploy-backend verify-backend deploy-frontend verify-frontend

# Target to build and deploy the backend using Google Cloud Build
deploy-backend:
	@echo "Building and deploying backend using Cloud Build..."
	@(cd backend; gcloud builds submit --config=cloudbuild.yaml . --substitutions="_AR_REGION=$(GOOGLE_CLOUD_LOCATION),_AR_REPO_NAME=$(GOOGLE_ADK_APP_REPOSITORY),_APP_NAME=$(GOOGLE_ADK_APP_NAME),_GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI),_FIREBASE_APP_URLS=$(FIREBASE_APP_URLS)")

# Target to verify the status of the deployed backend service
verify-backend:
	@echo "Verifying backend deployment status..."
	@gcloud run services describe "$(GOOGLE_ADK_APP_NAME)-service" --platform managed --region $(GOOGLE_CLOUD_LOCATION)

# Target to build and deploy the frontend
deploy-frontend:
	@echo "Fetching backend URL for $(GOOGLE_ADK_APP_NAME)-service..."
	@APP_BACKEND_URL=$$(gcloud run services describe $(GOOGLE_ADK_APP_NAME)-service --platform managed --region $(GOOGLE_CLOUD_LOCATION) --format='value(status.url)'); \
	if [ -z "$$APP_BACKEND_URL" ]; then \
		echo "Error: Failed to fetch backend URL or URL is empty. Please ensure backend is deployed and $(GOOGLE_ADK_APP_NAME)-service is the correct service name."; \
		exit 1; \
	fi; \
	echo "Using Backend URL: $$APP_BACKEND_URL"; \
	echo "Installing frontend dependencies..."; \
	(cd frontend; npm install); \
	echo "Building frontend with REACT_APP_BACKEND_URL=$$APP_BACKEND_URL..."; \
	(cd frontend; REACT_APP_BACKEND_URL="$$APP_BACKEND_URL" npm run build); \
	echo "Deploying frontend to Firebase Hosting..."; \
	(cd frontend; firebase deploy --only hosting)

# Target to verify the frontend deployment (list hosting sites)
verify-frontend:
	@echo "Listing Firebase Hosting sites..."
	@(cd frontend; firebase hosting:sites:list)

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
