#Base Docker image with uWSGI and Nginx for Flask applications in Python running in a single container
FROM tiangolo/uwsgi-nginx:python3.6

#By default, the application runs on port 80, you can choose a different port by uncommenting the LISTEN PORT and EXPOSE
ENV LISTEN_PORT 5000

EXPOSE 5000
# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/static
# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured in this case it will be 0)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

# Add app
COPY ./data_formatter /app/data_formatter
COPY ./main.py /app/main.py

# Add API files
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./requirements.txt /app/requirements.txt

# Define working directory
WORKDIR /app

# Install requirements
RUN pip3 install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh

# Copy the entrypoint that will generate Nginx additional configs
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run the start script provided by the parent image tiangolo/uwsgi-nginx which in turn will start Nginx and uWSGI
CMD ["/start.sh"]