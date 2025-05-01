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
ARG GOOGLE_GENAI_USE_VERTEXAI
ARG GOOGLE_CLOUD_PROJECT
ARG GOOGLE_CLOUD_LOCATION

# Set runtime environment variables using the values from the build arguments (ARG).
# These ENV variables will be available to the application when the container runs.
ENV PATH="/home/myuser/.local/bin:$PATH"
ENV GOOGLE_GENAI_USE_VERTEXAI=${GOOGLE_GENAI_USE_VERTEXAI}
ENV GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
ENV GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}

# Set up environment variables - End

# Install ADK and dependencies - Start

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
# Use --user flag to install packages into the user's home directory (~/.local)
# This is important because we are running as a non-root user.
RUN pip install --user -r requirements.txt

# Install ADK - End

# Copy agent code - Start

# Copy the necessary application code (agent and utils) into the container
COPY __init__.py /app/agents/__init__.py
COPY simple_agent/ /app/agents/simple_agent/
COPY utils/ /app/agents/utils/

# Copy agent - End

# Define the command to run when the container starts
# $PORT is an environment variable automatically set by Cloud Run
CMD adk web --port=$PORT   "/app/agents"
