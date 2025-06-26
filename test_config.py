# Configuration loader that reads from .env file
import os

# Get environment from environment variable (can be overridden from command line)
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")

# Get URLs from environment variables
baseURLs = {
    "local": os.environ.get("LOCAL_URL", "http://localhost:5500"),
    "prod": os.environ.get("PROD_URL", "https://anupam.de")
}
