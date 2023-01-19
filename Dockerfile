FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP main.py
ENV FLASK_ENV development

# Create and set working directory
RUN mkdir /our_scheduler
WORKDIR /our_scheduler

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Expose port and run the app
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
