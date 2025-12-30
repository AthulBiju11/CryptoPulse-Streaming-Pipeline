# 1. Use a lightweight Python base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy everything from the CURRENT folder (producer/) into /app
# Since we will 'cd' into producer/, '.' refers to producer.py, requirements.txt, etc.
COPY . /app/

# 4. Install requirements
RUN pip install --no-cache-dir azure-eventhub websocket-client python-dotenv

# 5. Run the script
# We use -u to make sure Python logs appear in Azure immediately
CMD ["python", "-u", "producer.py"]