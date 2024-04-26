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

# Install any needed packages specified in requirements.txt
RUN pip install pytest
RUN pip install virtualhome
RUN pip install -e .

# Download and unzip the virtualhome simulator executable
# RUN wget -q http://virtual-home.org//release/simulator/last_release/linux_exec.zip -O \
#    /tmp/linux_exec.zip \
#    && unzip /tmp/linux_exec.zip -d /app/virtualhome/simulation \
#    && rm /tmp/linux_exec.zip

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
# ENV OPENAI_API_KEY=your_key_here

# Run app.py when the container launches
# CMD ["streamlit", "run", "src/assistants.py"]
CMD ["python3", "scripts/virtualhome_test.py"]
