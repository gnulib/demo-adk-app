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

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
# Use --user flag to install packages into the user's home directory (~/.local)
# This is important because we are running as a non-root user.
RUN pip install --user -r requirements.txt

# Install ADK - End

# Copy application code - Start

# Copy the main application, API, and utility modules
COPY main.py .
COPY api/ /app/api/
COPY utils/ /app/utils/ # Adjusted path for main.py and api/ to find utils

# The following files are kept as per the original Dockerfile structure.
# They might be related to ADK components or other parts of the application.
COPY __init__.py /app/agents/__init__.py
COPY simple_agent/ /app/agents/simple_agent/

# Copy application code - End

# Define the command to run when the container starts
# $PORT is an environment variable typically provided by the hosting environment (e.g., Cloud Run)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
