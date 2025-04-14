FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default values for environment variables
ENV SPOTIFY_CLIENT_ID="replace_with_client_id" \
    SPOTIFY_CLIENT_SECRET="replace_with_client_secret" \
    SPOTIFY_REDIRECT_URI="http://localhost:3000" \
    MONGODB_URI="mongodb://localhost:27017/"

# Create conf.yaml from environment variables at container start
RUN echo '#!/bin/bash\n\
echo "spotify:\n\
  client_id: $SPOTIFY_CLIENT_ID\n\
  client_secret: $SPOTIFY_CLIENT_SECRET\n\
  redirect_uri: $SPOTIFY_REDIRECT_URI\n\
\n\
mongodb:\n\
  uri: $MONGODB_URI" > /app/spotify_advance/apis/conf.yaml\n\
\n\
exec "$@"' > /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

# Expose the port that FastAPI will run on
EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
