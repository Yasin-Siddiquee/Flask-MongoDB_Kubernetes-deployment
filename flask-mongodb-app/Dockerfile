FROM python:3.8-slim

# Sets the working directory inside the container.
WORKDIR /app

# Copies the requirements file into the container.
COPY requirements.txt .

# Installs the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copies the entire application code into the container.
COPY . .

# Set environment variables for Flask.
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Exposes port 5000.
EXPOSE 5000

# Runs the Flask application.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
