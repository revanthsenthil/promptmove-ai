# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip

# Copy the current directory contents into the container at /app
COPY . /app

# Resolve Ubuntu portaudio issue
RUN apt-get update
RUN apt-get install portaudio19-dev -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install any needed packages specified in requirements.txt
RUN pip install pytest
# RUN pip install virtualhome
RUN pip install -e .

RUN cd src
RUN wget http://virtual-home.org//release/simulator/v2.0/v2.3.0/linux_exec.zip
RUN unzip linux_exec.zip -d linux_exec
RUN rm linux_exec.zip
RUN rm /usr/local/lib/python3.9/site-packages/virtualhome/__init__.py
WORKDIR /app/src

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
# ENV OPENAI_API_KEY=your_key_here

# Run app.py when the container launches
CMD ["streamlit", "run", "assistants.py"]
# CMD ["python3", "scripts/virtualhome_test.py"]
