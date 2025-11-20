import os
import json
import boto3
# Assuming init_db and add_example_data are imported correctly
from collector import init_db, add_example_data 

# --- SECRETS LOADING ---
def load_secrets():
    """Fetches AWS secrets and loads them into the environment."""
    # This must run on module import so secrets are available immediately.
    try:
        SECRET_NAME = os.environ.get("SECRET_NAME", "your_secret_name")
        REGION_NAME = "us-east-1" # <<< CHANGE THIS TO YOUR AWS REGION
        
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=REGION_NAME)
        
        secret_response = client.get_secret_value(SecretId=SECRET_NAME)
        app_secrets = json.loads(secret_response['SecretString'])
        
        # Load secrets into environment variables
        for key, value in app_secrets.items():
            os.environ[key] = value
        
        print(f"Successfully loaded secrets for {SECRET_NAME}")
        
    except Exception as e:
        print(f"FATAL ERROR: Could not load secrets from AWS Secrets Manager: {e}")
        raise # Stop if secrets can't be loaded

# --- DATABASE INITIALIZATION ---
def initialize_database():
    """Initializes the database connection and tables."""
    try:
        init_db()
        add_example_data() 
        print("Database connection established and tables initialized.")
    except Exception as e:
        print(f"CRITICAL DB ERROR: Failed to initialize database: {e}")
        raise
        
# CRITICAL: Run load_secrets immediately on import
load_secrets()