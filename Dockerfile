# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on (5000)
EXPOSE 5000

# Set the environment variable to indicate production mode
ENV FLASK_ENV=production

# Command to run the application
CMD ["gunicorn", "-w", "4", "app:app", "-b", "0.0.0.0:5000"]
