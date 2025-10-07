# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port (not strictly necessary, but good practice)
EXPOSE 8000

# Use a shell command so $PORT env variable is expanded
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
