FROM python:3.12-slim

# Set environment variables to ensure python output is logged and bytecode isn't generated
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory for where all project files will live
WORKDIR /app

# Install system dependencies needed for mysqlclient and other potential packages
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the default Django port
EXPOSE 8000

# Set the working directory to where manage.py is located
WORKDIR /app/EComm

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
