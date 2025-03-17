# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the Flask app port
EXPOSE 5123

# Run the application
CMD ["python", "-u", "app.py"]
