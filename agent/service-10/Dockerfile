# Use a smaller base image as the builder stage
FROM python:3.9-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy just the requirements file to install dependencies
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use a smaller base image as the final stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the application code from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY service.py /app/

# Expose the port on which the application will run (8000)
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["python", "service.py"]
