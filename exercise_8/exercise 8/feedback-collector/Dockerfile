FROM python:3.8-slim

# working directory 
WORKDIR /app

# Copy the requirements 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy  directory into the container 
COPY src/ ./src

# Expose the port 
EXPOSE 5000

# Define the command to run the application
CMD ["python", "src/feedback_app.py"]

