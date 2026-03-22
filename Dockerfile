# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt (if it exists)
# RUN pip install --no-cache-dir -r requirements.txt

# Run the orchestrator agent by default
CMD ["python3", "agents/orchestrator_agent.py"]
