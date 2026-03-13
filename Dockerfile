# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variable for API key (to be passed at runtime)
ENV OPENAI_API_KEY=""

# Run the test by default
CMD ["python", "main.py", "test"]