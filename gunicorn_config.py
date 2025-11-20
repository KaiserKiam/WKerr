from config import initialize_database

# This Gunicorn hook runs AFTER the application module is loaded 
# but BEFORE the worker starts handling requests.
def post_worker_init(worker):
    """Initializes the database within the Gunicorn worker process."""
    initialize_database()
    worker.log.info("Database initialized successfully inside worker.")