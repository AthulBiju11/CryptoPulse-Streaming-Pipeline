# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy your producer and requirements
COPY producer/producer.py .
# If you don't have a requirements.txt, we will just install them directly

# 4. Install the necessary libraries
RUN pip install --no-cache-dir azure-eventhub websocket-client python-dotenv

# 5. Run the script
CMD ["python", "-u", "producer.py"]