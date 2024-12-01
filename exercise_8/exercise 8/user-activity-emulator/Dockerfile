FROM python:3.8-slim

# working directory
WORKDIR /app

# Copy the requirements
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy directories into the container at /app
COPY src/ ./src
COPY data/ ./data

# Expose port 5000
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "src/user_simulator_app.py"]
