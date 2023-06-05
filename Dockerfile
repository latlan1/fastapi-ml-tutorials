# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY api.py /app
COPY requirements.txt /app
COPY model.h5 /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
EXPOSE 8000
CMD ["python", "api.py"]

# docker build -t fastapi-test-app:new .
# docker run -p 8000:8000 fastapi:new