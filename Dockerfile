# Base Image
FROM python:3.9

WORKDIR /src

# Copy requirements.txt file
COPY ./requirements.txt /src/requirements.txt

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH=/src

# Copy source code
COPY ./src/app /src/app

# Copy and make entrypoint executable
COPY ./src/docker-entrypoint.sh /src/
RUN chmod +x /src/docker-entrypoint.sh

ENTRYPOINT ["/src/docker-entrypoint.sh"]
