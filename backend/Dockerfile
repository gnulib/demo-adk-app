FROM python:3.11-slim
WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password --gecos "" myuser

# Change ownership of /app to myuser
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Set up environment variables - Start
ENV PATH="/home/myuser/.local/bin:$PATH"

ENV GOOGLE_GENAI_USE_VERTEXAI=${GOOGLE_GENAI_USE_VERTEXAI}
ENV GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
ENV GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}

# Set up environment variables - End

# Install ADK - Start

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install ADK - End

# Copy agent - Start

COPY __init__.py /app/agents/__init__.py
COPY simple_agent/ /app/agents/simple_agent/
COPY utils/ /app/agents/utils/

# Copy agent - End

CMD adk web --port=$PORT   "/app/agents"
