FROM python:3.8-slim

# working directory 
WORKDIR /app

# Install build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential

# Copy the requirements.txt 
COPY requirements.txt requirements.txt

# Install the dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy  directories into the container 
COPY src/ ./src
COPY models/ ./models

# Expose port 5000 
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "src/recommender_app.py"]
