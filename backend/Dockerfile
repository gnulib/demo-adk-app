# Use the official Python slim image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Create a non-root user for security best practices
RUN adduser --disabled-password --gecos "" myuser

# Change ownership of the working directory to the non-root user
RUN chown -R myuser:myuser /app

# Switch to the non-root user for subsequent instructions
USER myuser

# Set up environment variables - Start

# Define build-time arguments for variables that will be injected during the Docker build process.
# These ARG instructions accept values passed via --build-arg during 'docker build'.

# Set runtime environment variables using the values from the build arguments (ARG).
# These ENV variables will be available to the application when the container runs.
ENV PATH="/home/myuser/.local/bin:$PATH"
# Environment variables for Google Cloud services (PROJECT, LOCATION, etc.)
# will be injected during the deployment process, not set in the Dockerfile.

# Set up environment variables - End

# Install ADK and dependencies - Start

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy the application code into the container
COPY src/ /app/src/

# Install the application as a module
RUN pip install  --no-cache-dir -r ./src/demo_adk_app/requirements.txt

# Install ADK - End

# set the working directory for the application
WORKDIR /app/src

# Define the command to run when the container starts
# $PORT is an environment variable typically provided by the hosting environment (e.g., Cloud Run)
CMD ["sh", "-c", "uvicorn demo_adk_app.main:app --host 0.0.0.0 --port $PORT"]
