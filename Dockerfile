# Use a specific, lightweight, and AMD64-compatible Python base image
# The --platform flag ensures compatibility as requested.
FROM --platform=linux/amd64 python:3.10-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Install the only required Python dependency.
# We use --no-cache-dir to keep the image size small.
# PyMuPDF is the library for the 'fitz' import.
RUN pip install --no-cache-dir PyMuPDF

# Copy the Python scripts into the container's working directory
COPY pdf_parser.py .
COPY main.py .

# Define the command to run when the container starts.
# This will execute the main script automatically.
CMD ["python", "main.py"]
